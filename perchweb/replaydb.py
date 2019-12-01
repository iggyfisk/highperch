""" Replay storage logic """

import os
import subprocess
import json
import sqlite3
from datetime import datetime
from hashlib import sha256
from flask import flash, g, current_app, request
from models.replay import Replay, ReplayListInfo
from perchlogging import log_to_slack, format_ip_addr, format_traceback
import filepaths


class ReplayParsingException(Exception):
    """Known parsing error with user readable message"""


context_db_key = '_wig_db'
context_rollback_key = '_wig_db_rollback'


def get_connection():
    """ Get a replay db connection, store it in the request context for reuse """
    wig_db = getattr(g, context_db_key, None)
    if wig_db is None:
        wig_db = sqlite3.connect(filepaths.get_db('wig.db'))
        wig_db.row_factory = sqlite3.Row
        setattr(g, context_db_key, wig_db)
    return wig_db


def query(query_text, args=(), one=False):
    """ Run query_text with args against the replay db, one=True for a single result row """
    cursor = get_connection().execute(query_text, args)
    results = cursor.fetchall()
    cursor.close()
    return (results[0] if results else None) if one else results


def close_connection():
    """ Cleanup when request is about to end """
    wig_db = getattr(g, context_db_key, None)
    if wig_db is not None:
        rollback = getattr(g, context_rollback_key, False)
        if not rollback:
            wig_db.commit()
        wig_db.close()
        setattr(g, context_db_key, None)


filter_sort_column = {
    'id': 'ID',
    'length': 'Length',
    'tower': 'TowerCount',
    'chat': 'ChatMessageCount'
}


def list_replays(search_filter):
    """ Search for replays to list on the index page """

    order_column = filter_sort_column.get(search_filter['sort'], None)
    if not order_column:
        # Bad sort order parameter, possibly malicious
        return []

    name_param = f"%{search_filter['name']}%" if search_filter['name'] else None
    map_param = f"%{search_filter['map']}%" if search_filter['map'] else None
    chat_param = f"%{search_filter['chat']}%" if search_filter['chat'] else None

    # Dynamic SQL hell yeah! It's perfectly safe but I'm not 100% about the performance
    # once we get to 100k replays, ideally only the active filters would be in the query text
    rows = query(f'''
    SELECT ID, Name, TimeStamp, Official, HighQuality, GameType, Version, Length, Map, TowerCount, ChatMessageCount,
        Towers, Players, Views, UploaderIP
    FROM Replays
    WHERE 
        (? = 0 OR Official = 1) AND
        (? IS NULL OR Name LIKE ?) AND
        (? IS NULL OR Map LIKE ?) AND
        (? IS NULL OR Chat LIKE ?)
    ORDER BY {order_column} DESC
    ''', (search_filter['official'], name_param, name_param, map_param, map_param, chat_param, chat_param))

    return [ReplayListInfo(**r) for r in rows]


def list_player_replays(battletag, max_results=5):
    """ Search for replays including a specific player """
    # Todo: combine key elements with list_replays
    rows = query('''
    SELECT ID, Name, TimeStamp, Official, HighQuality, GameType, Version, Length, Map, R.TowerCount, R.ChatMessageCount,
        Towers, Players, Views
    FROM Replays AS R
    INNER JOIN GamesPlayed ON ReplayID = ID
    WHERE PlayerTag = ?
    ORDER BY ID DESC
    LIMIT ?
    ''', (battletag, max_results))

    return [ReplayListInfo(**r) for r in rows]


def get_replay_listinfo(replay_id, inc_views=False, inc_downloads=False):
    """ Load the highper.ch info for a single replay from DB (name, views etc) """
    if inc_views:
        query(
            'UPDATE Replays SET Views = Views + 1 WHERE ID = ?', (replay_id,))
    if inc_downloads:
        query(
            'UPDATE Replays SET Downloads = Downloads + 1 WHERE ID = ?', (replay_id,))

    row = query('''
        SELECT Name, TimeStamp, HighQuality, Views, UploaderIP, VODURL
        FROM Replays
        WHERE ID = ?
        ''', (replay_id,), one=True)

    return ReplayListInfo(**row) if row is not None else None


def get_replay(replay_id):
    """ Load full replay data from JSON, only contains data from the original .w3g """
    data_path = filepaths.get_replay_data(f"{replay_id}.json")

    if not os.path.isfile(data_path):
        return None

    with open(data_path, encoding='utf8') as replay_json:
        replay_data = Replay(**json.load(replay_json))
    return replay_data


def get_player(battletag):
    """ Load some aggregated info for a specific player """

    player_row = query('''
        SELECT HUGames, ORGames, NEGames, UDGames
        FROM Players
        WHERE BattleTag = ?
        ''', (battletag,), one=True)

    if player_row is None:
        return None

    aggregate_row = query('''
        SELECT CAST(AVG(APM) AS INTEGER) AS AvgApm, SUM(TowerCount) AS TowerCount, SUM(ChatMessageCount) AS ChatMessageCount,
	        SUM(CASE WHEN NetGoldFed > 0 THEN NetGoldFed ELSE 0 END) AS GoldSent,
	        SUM(CASE WHEN NetLumberFed > 0 THEN NetLumberFed ELSE 0 END) AS LumberSent
        FROM GamesPlayed
        WHERE PlayerTag = ?
        GROUP BY PlayerTag
    ''', (battletag,), one=True)

    if aggregate_row is None:
        # Would only happen if someone was part of only 1 replay, which got deleted
        return None

    return dict(**player_row, **aggregate_row)


def create_players(battletags):
    """ Make sure all players in a replay have a player row """
    for tag in battletags:
        query('INSERT OR IGNORE INTO Players(BattleTag) VALUES(?)', (tag,))


def save_game_played(replay_data, replay_id):
    """ Record player participation in a replay """
    for player in replay_data.players:
        name = player['name']
        race = (player['raceDetected'] or player['race'])
        apm = player['apm']
        win = player['teamid'] == replay_data['winningTeamId'] if replay_data['winningTeamConfirmed'] else None
        tower_count = player.tower_count()
        chat_count = sum(
            1 for c in replay_data['chat'] if c['playerId'] == player['id'])
        net_feed = player.net_feed()
        net_gold = net_feed[0]
        net_lumber = net_feed[1]
        first_share = player.first_share()

        query('''
            INSERT INTO GamesPlayed (PlayerTag, ReplayID, Race, APM, Win, TowerCount, ChatMessageCount, NetGoldFed, NetLumberFed, TimeToShare)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (name, replay_id, race, apm, win, tower_count, chat_count, net_gold, net_lumber, first_share))

        # Only record when the players real race was detected, otherwise they weren't really playing
        if race != 'R':
            col = {'H': 'HUGames', 'O': 'ORGames',
                   'N': 'NEGames', 'U': 'UDGames'}[race]
            query(
                f'UPDATE Players SET {col} = {col} + 1 WHERE BattleTag = ?', (name,))


def save_replay(replay, replay_name, uploader_ip):
    """ Parse and save replay file """
    timestamp = int(datetime.now().timestamp())
    unique = int.from_bytes(os.urandom(2), 'little')
    temp_replay_path = filepaths.get_temp(f'{unique}_{timestamp}.w3g')
    temp_data_path = filepaths.get_temp(f'{unique}_{timestamp}.json')
    replay.save(temp_replay_path)

    # From here on out we need to clean up if anything goes wrong
    try:
        with open(temp_replay_path, 'rb') as replay_bytes:
            file_hash = sha256(replay_bytes.read()).hexdigest()

        dupe_check = query(
            'SELECT Name FROM Replays WHERE FileHash=?;', (file_hash,), one=True)
        if dupe_check:
            error_string = f'Attempted duplicate upload from {format_ip_addr(request.remote_addr)}: "{replay_name}"'
            log_to_slack('WARNING', error_string)
            current_app.logger.warning(error_string)
            raise ReplayParsingException(
                f"Replay already exists: {dupe_check[0]}")

        parse_result = subprocess.run(
            ["node", filepaths.get_path("../parsereplay.js"), temp_replay_path, temp_data_path])
        if parse_result.returncode > 0:
            raise ReplayParsingException("Replay parsing failed")

        with open(temp_data_path, encoding='utf8') as replay_json:
            replay_data = Replay(**json.load(replay_json))

        # Todo: more validation, like gametype and version,
        # maybe the battletag that saved the replay is banned

        # Not the best connection to the ReplayListInfo class
        bnet_id = replay_data['id']
        gametype = replay_data['type']
        version = replay_data['version']
        length = replay_data['duration']
        map_name = replay_data.map_name()

        players = [{'name': p['name'], 'teamid': p['teamid'], 'race': (p['raceDetected'] or p['race'])}
                   for p in replay_data.players]
        create_players([p['name'] for p in players])

        official = 1 if replay_data.official() else 0
        towers = replay_data.get_drawmap(force=True)['towers']
        # concatenate one big string that can be searched through later
        chat = '|'.join([c['message'] for c in replay_data['chat']])
        tower_count = replay_data.tower_count()
        chat_message_count = len(replay_data['chat'])
        uploader_battletag = [
            p['name'] for p in replay_data.players if p['id'] == replay_data['saverPlayerId']][0]

        query('''
            INSERT INTO Replays(BNetGameID, Name, TimeStamp, Official, GameType, Version, Length, Map,
            TowerCount, ChatMessageCount, Players, Towers, Chat, UploaderBattleTag, UploaderIP, FileHash)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bnet_id, replay_name, timestamp, official, gametype, version, length, map_name,
                  tower_count, chat_message_count, json.dumps(players), json.dumps(towers), chat, uploader_battletag, uploader_ip, file_hash))
        replay_id = query('SELECT last_insert_rowid()', one=True)[0]

        save_game_played(replay_data, replay_id)

        replay_path = filepaths.get_replay(f"{replay_id}.w3g")
        data_path = filepaths.get_replay_data(f"{replay_id}.json")
        os.rename(temp_replay_path, replay_path)
        os.rename(temp_data_path, data_path)

        flash('Replay uploaded')
        return replay_id
    except ReplayParsingException as err:
        flash(str(err))
        setattr(g, context_rollback_key, True)
    except Exception as e:
        error_string = f'Failed upload from {format_ip_addr(request.remote_addr)}: "{replay_name}"\nError follows:\n{format_traceback(e)}'
        log_to_slack('WARNING', error_string)
        current_app.logger.warning(error_string)
        flash("Failed, don't try again")
        setattr(g, context_rollback_key, True)
    finally:
        if os.path.isfile(temp_replay_path):
            os.remove(temp_replay_path)
        if os.path.isfile(temp_data_path):
            os.remove(temp_data_path)


def delete_replay(replay_id):
    """ Deletes a replay from disk and db, returns True on success """

    replay_path = filepaths.get_replay(f"{replay_id}.w3g")
    data_path = filepaths.get_replay_data(f"{replay_id}.json")
    try:
        # Any related chatlogs and pics can stay, but they're no longer related
        query('UPDATE Chatlogs SET ReplayID = NULL WHERE ReplayID = ?', (replay_id,))
        query('UPDATE Pics SET ReplayID = NULL WHERE ReplayID = ?', (replay_id,))

        # Remove player participation and reduce games played counts
        def update_race_count(race):
            col = {'H': 'HUGames', 'O': 'ORGames',
                   'N': 'NEGames', 'U': 'UDGames'}[race]
            query(f'''
                UPDATE Players
                SET {col} = {col} - 1
                WHERE EXISTS(SELECT PlayerTag
                    FROM GamesPlayed AS G
                    WHERE PlayerTag = BattleTag
                    AND G.ReplayID = ?
                    AND G.Race = ?);''', (replay_id, race))

        update_race_count('H')
        update_race_count('O')
        update_race_count('N')
        update_race_count('U')

        query('DELETE FROM GamesPlayed WHERE ReplayID = ?', (replay_id,))

        # Remove replay
        query('DELETE FROM Replays WHERE ID = ?', (replay_id,))

        os.remove(replay_path)
        os.remove(data_path)
        flash('Replay deleted')
        return True
    except Exception as e:
        error_string = f'Failed deletion from {format_ip_addr(request.remote_addr)}: ID {replay_id}"\nError follows:\n{format_traceback(e)}'
        log_to_slack('WARNING', error_string)
        current_app.logger.warning(error_string)
        flash('Unable to delete replay, error follows')
        flash(str(e))
        setattr(g, context_rollback_key, True)

    return False


def save_chatlog(replay_id, chat):
    """ Immortalizes a particularly sick chat """

    query('''
        INSERT INTO Chatlogs (ReplayID, ChatText)
        VALUES (?,?)''', (replay_id, chat))
