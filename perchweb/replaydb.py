""" Replay storage logic """

import os
import subprocess
import json
import sqlite3
from datetime import datetime
from flask import flash, g
from perchweb import app
from perchweb.models.replay import Replay, ReplayListInfo


class ReplayParsingException(Exception):
    """Known parsing error with user readable message"""


def get_wig_db():
    db = getattr(g, '_wig_database', None)
    if db is None:
        db = g._wig_database = sqlite3.connect('wig.db')
        db.row_factory = sqlite3.Row
    return db


def query_wig_db(query, args=(), one=False):
    cursor = get_wig_db().execute(query, args)
    results = cursor.fetchall()
    cursor.close()
    return (results[0] if results else None) if one else results


@app.teardown_appcontext
def close_connection(exception):
    wig_db = getattr(g, '_wig_database', None)
    if wig_db is not None:
        wig_db.commit()
        wig_db.close()


def list_replays(filter):
    rows = query_wig_db('''
    SELECT ID, Name, TimeStamp, GameType, Version, Length, Map, TowerCount, ChatMessageCount, Players, Views
    FROM Replays
    ORDER BY ID DESC
    ''')

    return [ReplayListInfo(**r) for r in rows]


def get_replay_listinfo(replay_id, inc_views=False):
    """ Load the web-specific replay info from DB """
    if inc_views:
        query_wig_db(
            'UPDATE Replays SET Views = Views + 1 WHERE ID = ?', (replay_id,))

    row = query_wig_db('''
        SELECT Name, TimeStamp, Views
        FROM Replays
        WHERE ID = ?
        ''', (replay_id,), one=True)

    return ReplayListInfo(**row) if row is not None else None


def get_replay(replay_id):
    """ Load full replay data from JSON """
    # Todo: solid configurable data directories
    data_path = os.path.join('replaydata', f"{replay_id}.json")

    if not os.path.isfile(data_path):
        return None

    with open(data_path) as replay_json:
        replay_data = Replay(**json.load(replay_json))
    return replay_data


def save_replay(replay, replay_filename, replay_filename_parts, replay_name):
    """ Parse and save replay file """
    # Todo: solid configurable temp directory
    temp_replay_path = os.path.join('temp', replay_filename)
    temp_data_path = os.path.join('temp', f'{replay_filename_parts[0]}.json')
    replay.save(temp_replay_path)

    # From here on out we need to clean up if anything goes wrong
    try:
        parse_result = subprocess.run(
            ["node", "parsereplay.js", temp_replay_path, temp_data_path])
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
        chat = [c['message'] for c in replay_data['chat']]
        tower_count = replay_data.tower_count()
        chat_message_count = len(chat)

        # Todo: json() function when sqlite supports it everywhere
        query_wig_db('''
            INSERT INTO Replays(BNetGameID, Name, TimeStamp, GameType, Version, Length, Map, TowerCount, ChatMessageCount, Players, Chat)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bnet_id, replay_name, timestamp, gametype, version, length, map_name, tower_count, chat_message_count,
                  json.dumps(players), json.dumps(chat)))

        replay_id = query_wig_db('SELECT last_insert_rowid()', one=True)[0]

        # Todo: solid configurable data directories
        replay_path = os.path.join(
            'perchweb', 'static', 'replays', f"{replay_id}.w3g")
        data_path = os.path.join('replaydata', f"{replay_id}.json")
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
