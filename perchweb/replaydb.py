""" Replay storage logic """

import os
import subprocess
import json
import sqlite3
import glob
from datetime import datetime
from hashlib import sha256
from collections import defaultdict
from ipaddress import ip_address, ip_network
from statistics import mean
from re import search as re_search
from flask import flash, g, current_app, request
from models.replay import Replay, ReplayListInfo
from perchlogging import log_to_slack, upload_to_slack, format_ip_addr, format_traceback
from lib.wigcodes import get_map_canonical_name, untranslate_map_name
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

    try:
        limit = int(search_filter['max_size'])
        limit = limit if limit > 0 and limit < 10000 else 100
    except ValueError:
        limit = 100
    try:
        offset = int(search_filter['from'])
        offset = offset if offset > 0 else 0
    except ValueError:
        offset = 0

    name_param = f"%{search_filter['name']}%" if search_filter['name'] else None
    map_param = f"%{search_filter['map']}%" if search_filter['map'] else None
    chat_param = f"%{search_filter['chat']}%" if search_filter['chat'] else None
    player_name_param = f"%{search_filter['player_name']}%" if search_filter['player_name'] else None
    nsearch = player_name_param is not None

    # Only include the play name param if this is a name search
    params = (search_filter['official'], search_filter['hasvod'], name_param, name_param,
              map_param, map_param, chat_param, chat_param, player_name_param)[:None if nsearch else -1]
    # Dynamic SQL hell yeah! It's perfectly safe but I'm not 100% about the performance
    # once we get to 100k replays, ideally only the active filters would be in the query text
    rows = query(f'''
        SELECT {"Distinct" if nsearch else ""} ID, Name, TimeStamp, Official, HighQuality, GameType, Version, Length, Map,
            R.TowerCount, R.ChatMessageCount, Towers, StartLocations, Players, Views, UploaderIP, UploaderBattleTag, VODURL
        FROM Replays AS R
        {"INNER JOIN GamesPlayed AS GP ON GP.ReplayID = ID" if nsearch else ""}
        WHERE 
            (? = 0 OR Official = 1) AND
            (? = 0 OR VODURL IS NOT NULL) AND
            (? IS NULL OR Name LIKE ?) AND
            (? IS NULL OR Map LIKE ?) AND
            (? IS NULL OR Chat LIKE ?)
            {"AND GP.PlayerTag LIKE ?" if nsearch else ""}
        ORDER BY {order_column} DESC
        LIMIT {offset}, {limit}
        ''', params)

    return [ReplayListInfo(**r) for r in rows]


def count_replays(search_filter):
    """ Total number of matching replays currently in the database """
    name_param = f"%{search_filter['name']}%" if search_filter['name'] else None
    map_param = f"%{search_filter['map']}%" if search_filter['map'] else None
    chat_param = f"%{search_filter['chat']}%" if search_filter['chat'] else None
    player_name_param = f"%{search_filter['player_name']}%" if search_filter['player_name'] else None
    nsearch = player_name_param is not None

    # Only include the play name param if this is a name search
    params = (search_filter['official'], search_filter['hasvod'], name_param, name_param,
              map_param, map_param, chat_param, chat_param, player_name_param)[:None if nsearch else -1]
    total_count = query(f'''
        SELECT COUNT(DISTINCT ID) AS ReplayCount
        FROM Replays AS R
        {"INNER JOIN GamesPlayed AS GP ON GP.ReplayID = ID" if nsearch else ""}
        WHERE 
            (? = 0 OR Official = 1) AND
            (? = 0 OR VODURL IS NOT NULL) AND
            (? IS NULL OR Name LIKE ?) AND
            (? IS NULL OR Map LIKE ?) AND
            (? IS NULL OR Chat LIKE ?)
            {"AND GP.PlayerTag LIKE ?" if nsearch else ""}
        ''', params, one=True)['ReplayCount']

    return total_count


def list_player_replays(battletag, max_results=20):
    """ Search for replays including a specific player """
    # Todo: combine key elements with list_replays
    rows = query('''
    SELECT ID, Name, TimeStamp, Official, HighQuality, GameType, Version, Length, Map, R.TowerCount, R.ChatMessageCount,
        Towers, StartLocations, Players, Views, UploaderIP, VODURL
    FROM Replays AS R
    INNER JOIN GamesPlayed ON ReplayID = ID
    WHERE PlayerTag = ?
    ORDER BY ID DESC
    LIMIT ?
    ''', (battletag, max_results))

    return [ReplayListInfo(**r) for r in rows]


def list_map_replays(map_name, max_results=20):
    """ Search for replays on a specific map """
    # Todo: combine key elements with list_replays
    rows = query('''
    SELECT ID, Name, TimeStamp, Official, HighQuality, GameType, Version, Length, Map, TowerCount, ChatMessageCount,
        Towers, StartLocations, Players, Views, UploaderIP, VODURL
    FROM Replays
    WHERE Map = ? COLLATE NOCASE
    ORDER BY ID DESC
    LIMIT ?
    ''', (map_name, max_results))

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


def get_all_replays():
    """ Full replay data for every processed reep"""
    replays = []
    for data_path in glob.glob(filepaths.get_replay_data('*.json')):
        with open(data_path, encoding='utf8') as replay_json:
            replays.append(Replay(**json.load(replay_json)))
    return replays


def get_player(battletag):
    """ Load some aggregated info for a specific player """

    player_row = query('''
        SELECT HUGames, ORGames, NEGames, UDGames, RDGames
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


def get_map(map_name):
    """ Load some aggregated info for a specific map """

    return query('''
        SELECT GameType, Count(*) AS Games, CAST(AVG(Length) AS INT) AS AvgLength, CAST(AVG(TowerCount) AS INT) AS AvgTowers
        FROM Replays
        WHERE (Map = ? OR Map = ?) COLLATE NOCASE
        GROUP BY GameType
        ''', (untranslate_map_name(map_name), map_name))


def get_game_count(replay_id):
    """ Get total games played for all players in a replay """
    result = query('''
            SELECT G1.PlayerTag, COUNT(*)
            FROM GamesPlayed AS G1
			INNER JOIN GamesPlayed G2 ON G1.PlayerTag = G2.PlayerTag AND G2.ReplayID = ?
			GROUP BY G1.PlayerTag;''', (replay_id,))
    return {r[0]: r[1] for r in result}


def create_players(battletags, query_fnc=query):
    """ Make sure all players in a replay have a player row """
    for tag in battletags:
        query_fnc('INSERT OR IGNORE INTO Players(BattleTag) VALUES(?)', (tag,))


def save_game_played(replay_data, replay_id, query_fnc=query):
    """ Record player participation in a replay """
    for player in replay_data.players:
        name = player['name']
        race = (player['race'])
        apm = player.get_real_apm()
        win = player['teamid'] == replay_data['winningTeamId'] if replay_data['winningTeamConfirmed'] else None
        tower_count = player.tower_count()
        chat_count = sum(
            1 for c in replay_data['chat'] if c['playerId'] == player['id'])
        net_feed = player.net_feed()
        net_gold = net_feed[0]
        net_lumber = net_feed[1]
        first_share = player.first_share()

        query_fnc('''
            INSERT INTO GamesPlayed (PlayerTag, ReplayID, Race, APM, Win, TowerCount, ChatMessageCount, NetGoldFed, NetLumberFed, TimeToShare)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (name, replay_id, race, apm, win, tower_count, chat_count, net_gold, net_lumber, first_share))

        increment_race_played(name, race, 1, query_fnc)


def delete_game_played(replay_id, query_fnc):
    """ Remove player data for a specific replay, to be reinserted by reparse """
    player_races = query_fnc(
        'SELECT PlayerTag, Race FROM GamesPlayed WHERE ReplayID = ?', (replay_id,))
    for player in player_races:
        increment_race_played(player['PlayerTag'],
                              player['Race'], -1, query_fnc)
    query_fnc('DELETE FROM GamesPlayed WHERE ReplayID = ?', (replay_id,))


def increment_race_played(player_name, race, increment, query_fnc):
    """ Add/Remove to total games played with race for a player """
    col = {'H': 'HUGames', 'O': 'ORGames',
            'N': 'NEGames', 'U': 'UDGames',
            'R': 'RDGames'}[race]
    query_fnc(
        f'UPDATE Players SET {col} = {col} + ? WHERE BattleTag = ?', (increment, player_name))


def fix_battletags(tags, query_fnc, fp):
    """ Find incomplete battletags and move them to the new correct version,
        for the entire database or the list of correct tags given"""
    query_text = '''
            SELECT OldPlayer.*, NewPlayer.BattleTag AS NewBattleTag
            FROM Players AS OldPlayer
            INNER JOIN Players AS NewPlayer
	            ON instr(NewPlayer.BattleTag, OldPlayer.BattleTag) = 1
                    AND NewPlayer.BattleTag <> OldPlayer.BattleTag'''

    for (ix, tag) in enumerate(tags):
        query_text += f' {"WHERE" if not ix else "OR"} NewPlayer.BattleTag = "{tag}"'

    for tag_match in query_fnc(query_text):
        old_tag = tag_match['BattleTag']
        new_tag = tag_match['NewBattleTag']
        log_to_slack('INFO',
                     f'Moving player {old_tag} to {new_tag}')

        replay_ids = query_fnc(
            'SELECT ReplayID FROM GamesPlayed WHERE PlayerTag = ?', (old_tag,))
        for row in replay_ids:
            replay_id = row['ReplayID']
            data_path = fp.get_replay_data(f"{replay_id}.json")
            with open(data_path, encoding='utf8') as replay_json:
                data_content = replay_json.read().replace(old_tag, new_tag)

            with open(data_path, "w", encoding='utf8') as replay_json:
                replay_json.write(data_content)

            players = query_fnc(
                'SELECT Players FROM Replays WHERE ID = ?', (replay_id,))
            players_content = players[0]['Players'].replace(old_tag, new_tag)
            query_fnc('UPDATE Replays set Players = ? WHERE ID = ?',
                      (players_content, replay_id))

        query_fnc('''UPDATE Players
            SET
                HUGames = HUGames + ?,
                ORGames = ORGames + ?,
                NEGames = NEGames + ?,
                UDGames = UDGames + ?,
                RDGames = RDGames + ?
            WHERE BattleTag = ?''', (tag_match['HUGames'], tag_match['ORGames'],
                                     tag_match['NEGames'], tag_match['UDGames'],
                                     tag_match['RDGames'],
                                     new_tag))

        query_fnc('''UPDATE GamesPlayed
            SET PlayerTag = ?
            WHERE PlayerTag = ?''', (new_tag, old_tag))

        query_fnc('''UPDATE Replays
            SET UploaderBattleTag = ?
            WHERE UploaderBattleTag = ?''', (new_tag, old_tag))

        query_fnc('DELETE FROM Players WHERE BattleTag = ?', (old_tag,))


def save_replay(replay, replay_name, uploader_ip):
    """ Parse and save replay file """
    timestamp = int(datetime.now().timestamp())
    unique = int.from_bytes(os.urandom(2), 'little')
    temp_replay_path = filepaths.get_temp(f'{unique}_{timestamp}.w3g')
    temp_data_path = filepaths.get_temp(f'{unique}_{timestamp}.json')
    replay.save(temp_replay_path)

    # From here on out we need to clean up if anything goes wrong
    try:
        parse_result = subprocess.run(
            ["node", filepaths.get_path("../parsereplay.js"), temp_replay_path, temp_data_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if parse_result.returncode != 0:
            error_string = f'Parser failure from {format_ip_addr(request.remote_addr)} - "{replay_name}":\n{parse_result.stderr.decode("utf-8")}'
            log_to_slack('ERROR', error_string)
            current_app.logger.warning(error_string)
            raise ReplayParsingException(
                "Replay parsing failed. If it's really a valid Reforged replay, let us know.")
        if len(parse_result.stdout) > 0:
            error_string = f'Parser warning from {format_ip_addr(request.remote_addr)} - "{replay_name}":\n{parse_result.stdout.decode("utf-8")}'
            log_to_slack('WARNING', error_string)
            current_app.logger.warning(error_string)
        with open(temp_data_path, encoding='utf8') as replay_json:
            replay_data = Replay(**json.load(replay_json))

        # Todo: more validation, like gametype and version

        # Not the best connection to the ReplayListInfo class
        bnet_id = replay_data['id']
        gametype = replay_data['type']
        version = replay_data['version']
        length = replay_data['duration']
        map_name = replay_data.map_name()

        players = [{'name': p['name'], 'teamid': p['teamid'], 'race': (p['raceDetected'] or p['race'])}
                   for p in replay_data.players]
        player_tags = [p['name'] for p in players]
        create_players(player_tags)
        # This new replay might include a corrected battletag from a beta-era replay
        fix_battletags(player_tags, query, filepaths)

        official = 1 if replay_data.official() else 0
        drawmap = replay_data.get_drawmap(force=True)
        towers = drawmap['towers']
        start_locations = drawmap['start_locations']
        # concatenate one big string that can be searched through later
        chat = '|'.join([c['message'] for c in replay_data['chat']])
        tower_count = replay_data.tower_count()
        chat_message_count = len(replay_data['chat'])
        if replay_data['saverPlayerId'] == -1:
            uploader_battletag = 'Unknown#0'
            error_string = f'Replay with unknown saver uploaded by {format_ip_addr(request.remote_addr)}: "{replay_name}"'
            log_to_slack('WARNING', error_string)
            current_app.logger.warning(error_string)
        else:
            uploader_battletag = [
                p['name'] for p in replay_data.players if p['id'] == replay_data['saverPlayerId']][0]

        if is_battletag_punished(uploader_battletag):
            error_string = f'Upload with punished BattleTag {uploader_battletag} from {format_ip_addr(request.remote_addr)}: "{replay_name}"'
            log_to_slack('WARNING', error_string)
            current_app.logger.warning(error_string)

        if is_battletag_banned(uploader_battletag):
            error_string = f'Attempted upload with banned saver BattleTag {uploader_battletag} from {format_ip_addr(request.remote_addr)}: "{replay_name}"'
            log_to_slack('WARNING', error_string)
            current_app.logger.warning(error_string)
            raise ReplayParsingException(
                f"We have declined to handle this replay. Email admin@highper.ch to discuss the terms")

        if is_ip_banned(request.remote_addr):
            error_string = f'Attempted upload from banned IP {format_ip_addr(request.remote_addr)}: "{replay_name}", saver {uploader_battletag}'
            log_to_slack('WARNING', error_string)
            current_app.logger.warning(error_string)
            raise ReplayParsingException(
                f"Upload declined: you have been banned! Email admin@highper.ch to discuss the terms")

        if replay_name_check(replay_name) == False:
            error_string = f'Bad replay name by {format_ip_addr(request.remote_addr)}: "{replay_name}", saver {uploader_battletag}'
            log_to_slack('WARNING', error_string)
            current_app.logger.warning(error_string)
            raise ReplayParsingException(
                f"That replay name sucks. Pick a better one")

        with open(temp_replay_path, 'rb') as replay_bytes:
            file_hash = sha256(replay_bytes.read()).hexdigest()
        dupe_check = query(
            'SELECT Name FROM Replays WHERE FileHash=?;', (file_hash,), one=True)
        if dupe_check:
            error_string = f'Attempted duplicate upload from {format_ip_addr(request.remote_addr)}: "{replay_name}", aka "{dupe_check[0]}", saver {uploader_battletag}'
            log_to_slack('WARNING', error_string)
            current_app.logger.warning(error_string)
            raise ReplayParsingException(
                f"Replay already exists: {dupe_check[0]}")

        query('''
            INSERT INTO Replays(BNetGameID, Name, TimeStamp, Official, GameType, Version, Length, Map,
            TowerCount, ChatMessageCount, Players, Towers, StartLocations, Chat, UploaderBattleTag, UploaderIP, FileHash)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bnet_id, replay_name, timestamp, official, gametype, version, length, map_name,
                  tower_count, chat_message_count, json.dumps(
                      players), json.dumps(towers), json.dumps(start_locations),
                  chat, uploader_battletag, uploader_ip, file_hash))
        replay_id = query('SELECT last_insert_rowid()', one=True)[0]

        save_game_played(replay_data, replay_id)

        replay_path = filepaths.get_replay(f"{replay_id}.w3g")
        data_path = filepaths.get_replay_data(f"{replay_id}.json")
        os.rename(temp_replay_path, replay_path)
        os.rename(temp_data_path, data_path)

        flash('Replay uploaded')
        return replay_id
    except ReplayParsingException as err:
        with open(temp_replay_path, 'rb') as replay_bytes:
            upload_to_slack(replay_name, replay_bytes.read())
        flash(str(err))
        setattr(g, context_rollback_key, True)
    except Exception as e:
        error_string = f'Failed upload from {format_ip_addr(request.remote_addr)}: "{replay_name}"\nError follows:\n[{e.__class__.__name__}]\n{format_traceback(e)}'
        log_to_slack('WARNING', error_string)
        current_app.logger.warning(error_string)
        with open(temp_replay_path, 'rb') as replay_bytes:
            upload_to_slack(replay_name, replay_bytes.read())
        flash("Looks like a legit replay but something broke, we'll look into it.")
        setattr(g, context_rollback_key, True)
    finally:
        if os.path.isfile(temp_replay_path):
            os.remove(temp_replay_path)
        if os.path.isfile(temp_data_path):
            os.remove(temp_data_path)


def reparse_replay(replay_id, query_fnc, fp):
    """ Re-parse an existing replay, save the new data and update DB """
    replay_path = fp.get_replay(f"{replay_id}.w3g")
    temp_data_path = fp.get_temp(f'{replay_id}.json')

    parse_result = subprocess.run(
        ["node", fp.get_path("../parsereplay.js"), replay_path, temp_data_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if parse_result.returncode > 0:
        raise ReplayParsingException(parse_result.stderr.decode("utf-8"))
    if len(parse_result.stdout) > 0:
        print(parse_result.stdout.decode("utf-8"))

    # From here on out we need to clean up if anything goes wrong
    try:
        with open(temp_data_path, encoding='utf8') as replay_json:
            replay_data = Replay(**json.load(replay_json))

        bnet_id = replay_data['id']
        gametype = replay_data['type']
        version = replay_data['version']
        length = replay_data['duration']
        map_name = replay_data.map_name(fp=fp)

        players = [{'name': p['name'], 'teamid': p['teamid'], 'race': (p['raceDetected'] or p['race'])}
                   for p in replay_data.players]
        create_players([p['name'] for p in players], query_fnc)

        official = 1 if replay_data.official() else 0
        drawmap = replay_data.get_drawmap(force=True, fp=fp)
        towers = drawmap['towers']
        start_locations = drawmap['start_locations']
        # concatenate one big string that can be searched through later
        chat = '|'.join([c['message'] for c in replay_data['chat']])
        tower_count = replay_data.tower_count()
        chat_message_count = len(replay_data['chat'])
        if replay_data['saverPlayerId'] == -1:
            uploader_battletag = 'Unknown#0'
        else:
            uploader_battletag = [
                p['name'] for p in replay_data.players if p['id'] == replay_data['saverPlayerId']][0]

        query_fnc('''
            UPDATE Replays
            SET 
                BNETGameID = ?,
                Official = ?,
                GameType = ?,
                Version = ?,
                Length = ?,
                Map = ?,
                TowerCount = ?,
                ChatMessageCount = ?,
                Players = ?,
                Towers = ?,
                StartLocations = ?,
                Chat = ?,
                UploaderBattleTag = ?
            WHERE ID = ?
            ''', (bnet_id, official, gametype, version, length, map_name,
                  tower_count, chat_message_count, json.dumps(players),
                  json.dumps(towers), json.dumps(start_locations),
                  chat, uploader_battletag, replay_id))

        delete_game_played(replay_id, query_fnc)
        save_game_played(replay_data, replay_id, query_fnc)

        data_path = fp.get_replay_data(f"{replay_id}.json")
        if os.path.isfile(data_path):
            os.remove(data_path)
        os.rename(temp_data_path, data_path)
    finally:
        if os.path.isfile(temp_data_path):
            os.remove(temp_data_path)


def edit_replay(replay_id, name=None):
    """ Edit replay db entry """
    previous_name = query(
        'SELECT Name FROM Replays WHERE ID = ?', (replay_id,), one=True)[0]
    query('UPDATE Replays SET Name = CASE WHEN ? IS NOT NULL THEN ? ELSE NAME END WHERE ID = ?',
          (name, name, replay_id,))
    error_string = f'Replay ID {replay_id} ("{previous_name}") renamed to "{name}" by {format_ip_addr(request.remote_addr)}'
    log_to_slack('WARNING', error_string)
    current_app.logger.warning(error_string)
    return True


def delete_replay(replay_id):
    """ Deletes a replay from disk and db, returns True on success """
    previous_name = query(
        'SELECT Name FROM Replays WHERE ID = ?', (replay_id,), one=True)[0]
    replay_path = filepaths.get_replay(f"{replay_id}.w3g")
    data_path = filepaths.get_replay_data(f"{replay_id}.json")
    try:
        # Any related chatlogs and pics can stay, but they're no longer related
        query('UPDATE Chatlogs SET ReplayID = NULL WHERE ReplayID = ?', (replay_id,))
        query('UPDATE Pics SET ReplayID = NULL WHERE ReplayID = ?', (replay_id,))

        # Remove player participation and reduce games played counts
        def update_race_count(race):
            col = {'H': 'HUGames', 'O': 'ORGames',
                   'N': 'NEGames', 'U': 'UDGames',
                   'R': 'RDGames'}[race]
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
        error_string = f'Replay ID {replay_id} ("{previous_name}") deleted by {format_ip_addr(request.remote_addr)}'
        log_to_slack('WARNING', error_string)
        current_app.logger.warning(error_string)
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


def save_vod_url(replay_id, vod_url):
    """ Add a VOD URL to the database """
    query('''UPDATE Replays SET VODURL = ? WHERE ID = ?''', (vod_url, replay_id))


def get_all_uploader_ips():
    rows = query(f'''
    SELECT UploaderIP
    FROM Replays
    ''')
    uploader_ips = defaultdict(int)
    for row in rows:
        uploader_ips[row[0]] += 1
    return sorted(uploader_ips.items(), key=lambda i: i[1], reverse=True)


def get_all_maps():
    maps = defaultdict(dict)
    rows = query('''
        SELECT Map, Count(*) AS Games, CAST(AVG(Length) AS INT) AS AvgLength, CAST(AVG(TowerCount) AS INT) AS AvgTowers
        FROM Replays
        GROUP BY Map
        ''')
    for map_name, count, avg_length, avg_towers in rows:
        canonical_name = get_map_canonical_name(map_name)
        if canonical_name in maps:
            current_count = maps[canonical_name]['count']
            maps[canonical_name]['count'] += count
            maps[canonical_name]['avg_length'] = (
                (maps[canonical_name]['avg_length'] * current_count) + (avg_length * count)) // maps[canonical_name]['count']
            maps[canonical_name]['avg_towers'] = (
                (maps[canonical_name]['avg_towers'] * current_count) + (avg_towers * count)) // maps[canonical_name]['count']
        else:
            maps[canonical_name]['count'] = count
            maps[canonical_name]['avg_length'] = avg_length
            maps[canonical_name]['avg_towers'] = avg_towers
    return [{'name': m, 'replay_count': maps[m]['count'], 'avg_length': maps[m]['avg_length'], 'avg_towers': maps[m]['avg_towers']} for m in maps]


def get_next_replay(this_id):
    next_id = query('''
            SELECT ID
            FROM Replays
            WHERE ID > ?
            ORDER BY ID
            LIMIT 1''', (this_id,), one=True)
    if next_id == None:
        return None
    return next_id[0]


def get_previous_replay(this_id):
    prev_id = query('''
            SELECT ID
            FROM Replays
            WHERE ID < ?
            ORDER BY ID DESC
            LIMIT 1''', (this_id,), one=True)
    if prev_id == None:
        return None
    return prev_id[0]


def save_banned_subnet(subnet, ip_addr, reason):
    timestamp = int(datetime.now().timestamp())
    query('''
        INSERT INTO BannedIPs (Subnet, OriginalIP, Reason, Timestamp)
        VALUES (?,?,?,?)''', (subnet, ip_addr, reason, timestamp))
    error_string = f'New ban by {format_ip_addr(request.remote_addr)}: {subnet} ({ip_addr}): "{reason}"'
    log_to_slack('WARNING', error_string)
    current_app.logger.warning(error_string)


def save_banned_account(battletag, reason):
    timestamp = int(datetime.now().timestamp())
    query('''
        INSERT INTO BannedAccounts (BattleTag, Reason, Timestamp)
        VALUES (?,?,?)''', (battletag, reason, timestamp))
    error_string = f'New ban by {format_ip_addr(request.remote_addr)}: {battletag}: "{reason}"'
    log_to_slack('WARNING', error_string)
    current_app.logger.warning(error_string)


def save_punished_account(battletag, reason):
    timestamp = int(datetime.now().timestamp())
    query('''
        INSERT INTO PunishedAccounts (BattleTag, Reason, Timestamp)
        VALUES (?,?,?)''', (battletag, reason, timestamp))
    error_string = f'New punishment by {format_ip_addr(request.remote_addr)}: {battletag}: "{reason}"'
    log_to_slack('WARNING', error_string)
    current_app.logger.warning(error_string)


def delete_subnet_ban(subnet):
    row = query(
        'SELECT OriginalIP, Reason from BannedIPs WHERE Subnet = ?', (subnet,), one=True)
    original_ip, reason = row[0], row[1]
    query('DELETE FROM BannedIPs WHERE Subnet = ?', (subnet,))
    error_string = f'Subnet ban on {subnet} ({original_ip}, {reason}) removed by {format_ip_addr(request.remote_addr)}'
    log_to_slack('WARNING', error_string)
    current_app.logger.warning(error_string)


def delete_account_ban(battletag):
    reason = query(
        'SELECT Reason FROM BannedAccounts WHERE BattleTag = ?', (battletag,), one=True)[0]
    query('DELETE FROM BannedAccounts WHERE BattleTag = ?', (battletag,))
    error_string = f'BattleTag ban on {battletag} ({reason}) removed by {format_ip_addr(request.remote_addr)}'
    log_to_slack('WARNING', error_string)
    current_app.logger.warning(error_string)


def delete_account_punishment(battletag):
    reason = query(
        'SELECT Reason FROM PunishedAccounts WHERE BattleTag = ?', (battletag,), one=True)[0]
    query('DELETE FROM PunishedACcounts WHERE BattleTag = ?', (battletag,))
    error_string = f'Punishment on {battletag} ({reason}) removed by {format_ip_addr(request.remote_addr)}'
    log_to_slack('WARNING', error_string)
    current_app.logger.warning(error_string)


def get_banned_subnets():
    rows = query(
        '''SELECT Subnet, OriginalIP, Reason, Timestamp FROM BannedIPs ORDER BY Timestamp DESC''')
    return [dict(row) for row in rows]


def get_banned_accounts():
    rows = query(
        '''SELECT BattleTag, Reason, Timestamp FROM BannedAccounts ORDER BY Timestamp DESC''')
    return [dict(row) for row in rows]


def get_punished_accounts():
    rows = query(
        '''SELECT BattleTag, Reason, Timestamp FROM PunishedAccounts ORDER BY Timestamp DESC''')
    return [dict(row) for row in rows]


def is_ip_banned(ip_addr):
    check_address = ip_address(ip_addr)
    subnets = [ip_network(entry['Subnet']) for entry in get_banned_subnets()]
    for subnet in subnets:
        if check_address in subnet:
            return True
    return False


def is_battletag_banned(battletag):
    if battletag in [entry['BattleTag'] for entry in get_banned_accounts()]:
        return True
    return False


def is_battletag_punished(battletag):
    if battletag in [entry['BattleTag'] for entry in get_punished_accounts()]:
        return True
    return False


key_grid = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'å'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.'],
]
vowels = ['a', 'e', 'i', 'o', 'u']
punctuation = ['.', '-', ',', '!', '?', ' ']
keys = {key: (x, y) for (y, row) in enumerate(key_grid)
        for (x, key) in enumerate(row)}
repeat_regex = r'([\w]{3,4})(\1){1,}'
number_regex = r'^\d+$'


def key_distance(a, b):
    if a in keys and b in keys:
        if a in vowels and a == b:
            return 2    # repeated vowels is fine
        return abs(keys[a][0] - keys[b][0]) + abs(keys[a][1] - keys[b][1])
    if ord(a) > 127 or ord(b) > 127:    # non-latin chars
        if a == b:
            return 1
        return 3        # this assumption seems reasonable
    return None


def string_complexity(user_string):
    lowered_string = user_string.lower()
    distance = [key_distance(lowered_string[i], lowered_string[i + 1])
                for i in range(len(lowered_string) - 1)]
    bonus = 0
    for char in user_string:
        bonus += 1 if char in punctuation else 0
    bonus += 1 if 'ffa' in user_string else 0
    bonus -= 1.5 if re_search(repeat_regex, user_string) else 0
    bonus -= 3 if re_search(number_regex, user_string) else 0
    return mean(d for d in distance if d is not None) + bonus


def replay_name_check(name):
    if string_complexity(name) <= 2:
        return False
    return True


def get_all_players():
    players = []
    rows = query('''
        SELECT PlayerTag, COUNT(PlayerTag) as PlayerGames, 
            CAST(AVG(APM) AS INTEGER) AS AvgApm, 
            CAST(AVG(TowerCount) AS INTEGER) AS TowerAvg, 
            SUM(TowerCount) AS TowerCount,
            SUM(Win) AS Wins,
            SUM(CASE WHEN RACE = "H" THEN 1 ELSE 0 END) AS HumanGames,
            SUM(CASE WHEN RACE = "O" THEN 1 ELSE 0 END) AS OrcGames,
            SUM(CASE WHEN RACE = "N" THEN 1 ELSE 0 END) AS ElfGames,
            SUM(CASE WHEN RACE = "U" THEN 1 ELSE 0 END) AS UndeadGames,
            SUM(CASE WHEN RACE = "R" THEN 1 ELSE 0 END) AS RandomGames,
            SUM(ChatMessageCount) AS ChatMessageCount,
            SUM(CASE WHEN NetGoldFed > 0 THEN NetGoldFed ELSE 0 END) AS GoldSent,
            SUM(CASE WHEN NetLumberFed > 0 THEN NetLumberFed ELSE 0 END) AS LumberSent,
            CAST(AVG(TimeToShare) AS INTEGER) AS TimetoShare
        FROM GamesPlayed
        GROUP BY PlayerTag
        ORDER BY PlayerGames;
        ''')

    for row in rows:
        player = dict(row)
        if player['Wins'] == None:
            player['Winrate'] = 0
        else:
            player['Winrate'] = int(round((player['Wins'] / player['PlayerGames']), 2) * 100)
        player['RaceGames'] = {'H': player['HumanGames'], 'O': player['OrcGames'], 
                               'N': player['ElfGames'], 'U': player['UndeadGames'],
                               'R': player['RandomGames']}
        player['RacePercent'] = {'H': round(player['HumanGames'] / player['PlayerGames'] * 100, 2),
                                 'O': round(player['OrcGames'] / player['PlayerGames'] * 100, 2),
                                 'N': round(player['ElfGames'] / player['PlayerGames'] * 100, 2),
                                 'U': round(player['UndeadGames'] / player['PlayerGames'] * 100, 2),
                                 'R': round(player['RandomGames'] / player['PlayerGames'] * 100, 2)}
        player['MaxRace'] = sorted(player['RacePercent'].values(), reverse=True)[0] * (1 + (player['PlayerGames'] / 500))
        del player['HumanGames']
        del player['OrcGames']
        del player['ElfGames']
        del player['UndeadGames']
        del player['RandomGames']
        player['AvgGoldSent'] = player['GoldSent'] // player['PlayerGames']
        player['AvgLumberSent'] = player['LumberSent'] // player['PlayerGames']
        player['AvgChatMessages'] = player['ChatMessageCount'] // player['PlayerGames']
        players.append(player)

    return players

def count_repeat_players():
    rows = query('''
        SELECT PlayerTag from GamesPlayed GROUP BY PlayerTag HAVING COUNT(*) > 1;
        ''')

    return len(rows)