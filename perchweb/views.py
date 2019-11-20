"""
Routes and views for the flask application.
"""

import random
import os
import subprocess
import json
import sqlite3
from datetime import datetime
from flask import url_for, request, redirect, flash, g
from werkzeug.utils import secure_filename
from perchweb import app
from perchweb.handler import standard_page
from perchweb.models.player import Player
from perchweb.models.replay import Replay


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


@app.route('/')
def index():
    """Index"""

    replays = [ 
        Replay("Quick 1v1", [Player("bimàldo goodmanners"), Player("iggy")]), 
        Replay("fours", [Player("mata"), Player("grubby"), Player("tillerman"), Player("th000")]), 
        Replay("comedy \"third\" game", [Player("timg4strok"), Player("AI (Easy)")])
    ]

    return standard_page('index.html', 'Replays', nav='index', replays=replays)


@app.route('/upload', methods=['POST'])
def upload_replay():
    """User replay uploads"""
    # Todo: Validation here, replay name, geoblocking etc
    replay_name = request.form['name']

    replay = request.files['replay'] if 'replay' in request.files else None
    replay_filename = secure_filename(
        replay.filename) if replay is not None else None
    if not replay_filename:
        flash('No replay file selected')
        return redirect(url_for('index'))

    replay_filename_parts = os.path.splitext(replay_filename)
    if len(replay_filename_parts) < 2 or replay_filename_parts[1] != '.w3g':
        flash('Not a .w3g replay')
        return redirect(url_for('index'))

    # Todo: Validation here, filesize etc

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
            replay_data = json.load(replay_json)

        # Todo: more validation, like gametype and version
        bnet_id = replay_data['id']
        timestamp = int(datetime.now().timestamp())
        gametype = replay_data['type']
        version = replay_data['version']
        length = replay_data['duration']
        map_name = replay_data['map']['file']
        map_name = os.path.splitext(os.path.basename(map_name))[0]
        players = [{
            'name': p['name'],
            'teamid': p['teamid'],
            'race': p['race'],
            'apm': p['apm'],
            'heroCount': p['heroCount']
        } for p in replay_data['players']]
        chat = [c['message'] for c in replay_data['chat']]
        # Todo: iterate over replay_data['players'][i]['buildings']['summary'] and add all the tower counts
        tower_count = 1
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
    return redirect(url_for('index'))


@app.route('/highperching')
def guide():
    """The art"""
    return standard_page('guide.html', 'The Art of Highperching', nav='guide')


# Todo: Store number of files, allow admin uploads etc
random.seed()
pic_max = 89
@app.route('/peep/', defaults={'pic_id': None})
@app.route('/peep/<int:pic_id>')
def peep(pic_id):
    """Sometimes random pictures"""
    pic_id = random.randint(1, pic_max) if pic_id is None else pic_id
    return standard_page('peep.html', 'Peep a pic', nav='peep',
                         pic_url=f'/static/images/peep/{pic_id}.jpg',
                         perma=url_for('peep', pic_id=pic_id))
