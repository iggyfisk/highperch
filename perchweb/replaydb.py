""" Replay storage logic """

import os
import subprocess
import json
import sqlite3
from datetime import datetime
from flask import flash, g
from models.replay import Replay, ReplayListInfo
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


def list_replays(search_filter):
    """ Search for replays to list on the index page """
    rows = query('''
    SELECT ID, Name, TimeStamp, Official, HighQuality, GameType, Version, Length, Map, TowerCount, ChatMessageCount, Players, Views
    FROM Replays
    ORDER BY ID DESC
    ''')

    return [ReplayListInfo(**r) for r in rows]


def list_player_replays(battletag):
    """ Search for replays including a specific player """
    # Todo: combine key elements with list_replays
    rows = query('''
    SELECT ID, Name, TimeStamp, Official, HighQuality, GameType, Version, Length, Map, R.TowerCount, R.ChatMessageCount, Players, Views
    FROM Replays AS R
    INNER JOIN GamesPlayed ON ReplayID = ID
    WHERE PlayerTag = ?
    ORDER BY ID DESC
    ''', (battletag,))

    return [ReplayListInfo(**r) for r in rows]


def get_replay_listinfo(replay_id, inc_views=False):
    """ Load the highper.ch info for a single replay from DB (name, views etc) """
    if inc_views:
        query(
            'UPDATE Replays SET Views = Views + 1 WHERE ID = ?', (replay_id,))

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

    with open(data_path) as replay_json:
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
        SELECT AVG(APM) AS AvgApm, SUM(TowerCount) AS TowerCount, SUM(ChatMessageCount) AS ChatMessageCount
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
        race = player['race']
        apm = player['apm']
        win = player['teamid'] == replay_data['winningTeamId'] if replay_data['winningTeamConfirmed'] else None
        tower_count = player.tower_count()
        chat_count = sum(
            1 for c in replay_data['chat'] if c['playerId'] == player['id'])

        query('''
            INSERT INTO GamesPlayed (PlayerTag, ReplayID, Race, APM, Win, TowerCount, ChatMessageCount)
            VALUES(?, ?, ?, ?, ?, ?, ?)''', (name, replay_id, race, apm, win, tower_count, chat_count))

        col = {'H': 'HUGames', 'O': 'ORGames',
               'N': 'NEGames', 'U': 'UDGames'}[race]
        query(
            f'UPDATE Players SET {col} = {col} + 1 WHERE BattleTag = ?', (name,))


def save_replay(replay, replay_filename, replay_filename_parts, replay_name, uploader_ip):
    """ Parse and save replay file """
    temp_replay_path = filepaths.get_temp(replay_filename)
    temp_data_path = filepaths.get_temp(f'{replay_filename_parts[0]}.json')
    replay.save(temp_replay_path)

    # From here on out we need to clean up if anything goes wrong
    try:
        parse_result = subprocess.run(
            ["node", filepaths.get_path("../parsereplay.js"), temp_replay_path, temp_data_path])
        if parse_result.returncode > 0:
            raise ReplayParsingException("Replay parsing failed")

        with open(temp_data_path) as replay_json:
            replay_data = Replay(**json.load(replay_json))

        # Todo: more validation, like gametype and version

        # Not the best connection to the ReplayListInfo class
        bnet_id = replay_data['id']
        timestamp = int(datetime.now().timestamp())
        gametype = replay_data['type']
        version = replay_data['version']
        length = replay_data['duration']
        map_name = replay_data.map_name()

        players = [{'name': p['name'], 'teamid': p['teamid'], 'race': p['race']}
                   for p in replay_data.players]
        create_players([p['name'] for p in players])

        official = 1 if replay_data.official() else 0
        # concatenate one big string that can be searched through later
        chat = '|'.join([c['message'] for c in replay_data['chat']])
        tower_count = replay_data.tower_count()
        chat_message_count = len(chat)
        uploader_battletag = [
            p['name'] for p in replay_data.players if p['id'] == replay_data['saverPlayerId']][0]
        # todo: real hash, should already have checked if it exists
        file_hash = os.urandom(32)

        query('''
            INSERT INTO Replays(BNetGameID, Name, TimeStamp, Official, GameType, Version, Length, Map,
            TowerCount, ChatMessageCount, Players, Chat, UploaderBattleTag, UploaderIP, FileHash)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bnet_id, replay_name, timestamp, official, gametype, version, length, map_name,
                  tower_count, chat_message_count, json.dumps(players), chat, uploader_battletag, uploader_ip, file_hash))
        replay_id = query('SELECT last_insert_rowid()', one=True)[0]

        save_game_played(replay_data, replay_id)

        replay_path = filepaths.get_replay(f"{replay_id}.w3g")
        data_path = filepaths.get_replay_data(f"{replay_id}.json")
        os.rename(temp_replay_path, replay_path)
        os.rename(temp_data_path, data_path)

        flash('Replay uploaded')
        # Todo: redirect to replay?
    except ReplayParsingException as err:
        flash(str(err))
        setattr(g, context_rollback_key, True)
    except Exception as e:
        # Todo: log error
        flash("Failed, don't try again")
        setattr(g, context_rollback_key, True)
    finally:
        if os.path.isfile(temp_replay_path):
            os.remove(temp_replay_path)
        if os.path.isfile(temp_data_path):
            os.remove(temp_data_path)
