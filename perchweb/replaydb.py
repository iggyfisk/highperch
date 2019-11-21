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


def get_connection():
    wig_db = getattr(g, context_db_key, None)
    if wig_db is None:        
        wig_db = sqlite3.connect(filepaths.get_db('wig.db'))
        wig_db.row_factory = sqlite3.Row
        setattr(g, context_db_key, wig_db)
    return wig_db


def query(query, args=(), one=False):
    cursor = get_connection().execute(query, args)
    results = cursor.fetchall()
    cursor.close()
    return (results[0] if results else None) if one else results


def close_connection():
    wig_db = getattr(g, context_db_key, None)
    if wig_db is not None:
        wig_db.commit()
        wig_db.close()
        setattr(g, context_db_key, None)


def list_replays(filter):
    rows = query('''
    SELECT ID, Name, TimeStamp, Official, GameType, Version, Length, Map, TowerCount, ChatMessageCount, Players, Views
    FROM Replays
    ORDER BY ID DESC
    ''')

    return [ReplayListInfo(**r) for r in rows]


def get_replay_listinfo(replay_id, inc_views=False):
    """ Load the web-specific replay info from DB """
    if inc_views:
        query(
            'UPDATE Replays SET Views = Views + 1 WHERE ID = ?', (replay_id,))

    row = query('''
        SELECT Name, TimeStamp, Views
        FROM Replays
        WHERE ID = ?
        ''', (replay_id,), one=True)

    return ReplayListInfo(**row) if row is not None else None


def get_replay(replay_id):
    """ Load full replay data from JSON """
    data_path = filepaths.get_replay_data(f"{replay_id}.json")

    if not os.path.isfile(data_path):
        return None

    with open(data_path) as replay_json:
        replay_data = Replay(**json.load(replay_json))
    return replay_data


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
        players = [{
            'name': p['name'],
            'teamid': p['teamid'],
            'race': p['race'],
            'apm': p['apm'],
            'heroCount': p['heroCount']
        } for p in replay_data['players']]
        official = 1 if replay_data.official() else 0
        chat = [c['message'] for c in replay_data['chat']]
        tower_count = replay_data.tower_count()
        chat_message_count = len(chat)

        # Todo: json() function when sqlite supports it everywhere
        query('''
            INSERT INTO Replays(BNetGameID, Name, TimeStamp, Official, GameType, Version, Length, Map, TowerCount, ChatMessageCount, Players, Chat, UploaderIP)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bnet_id, replay_name, timestamp, official, gametype, version, length, map_name, tower_count, chat_message_count,
                  json.dumps(players), json.dumps(chat), uploader_ip))

        replay_id = query(
            'SELECT last_insert_rowid()', one=True)[0]

        replay_path = filepaths.get_replay(f"{replay_id}.w3g")
        data_path = filepaths.get_replay_data(f"{replay_id}.json")
        os.rename(temp_replay_path, replay_path)
        os.rename(temp_data_path, data_path)

        flash('Replay uploaded')
        # Todo: redirect to replay?
    except ReplayParsingException as err:
        flash(str(err))
    except Exception as e:
        # Todo: log error
        flash("Failed, don't try again")
    finally:
        if os.path.isfile(temp_replay_path):
            os.remove(temp_replay_path)
        if os.path.isfile(temp_data_path):
            os.remove(temp_data_path)
