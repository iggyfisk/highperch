"""
Routes and views for the flask application.
"""

import random
import os
import subprocess
import json
from flask import url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from perchweb import app
from perchweb.handler import standard_page
from perchweb.models.player import Player
from perchweb.models.replay import Replay

class ReplayParsingException(Exception):
    """Known parsing error with user readable message"""

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

    replay = request.files['replay'] if 'replay' in request.files else None
    replay_filename = secure_filename(replay.filename) if replay is not None else None
    if not replay_filename:
        flash('No replay file selected')
        return redirect(url_for('index'))    
    
    replay_filename_parts = os.path.splitext(replay_filename)
    if len (replay_filename_parts) < 2 or replay_filename_parts[1] != '.w3g':
        flash('Not a .w3g replay')
        return redirect(url_for('index'))  

    # Todo: Validation here, filesize etc

    # Todo: solid configurable temp directory
    temp_replay_path = os.path.join('temp', replay_filename)
    temp_data_path = os.path.join('temp', f'{replay_filename_parts[0]}.json')
    replay.save(temp_replay_path)

    # From here on out we need to clean up if anything goes wrong
    try:
        parse_result = subprocess.run(["node", "parsereplay.js", temp_replay_path, temp_data_path])
        if parse_result.returncode > 0:
            raise ReplayParsingException("Replay parsing failed")

        with open(temp_data_path) as replay_json:
            replay_data = json.load(replay_json)

        flash(replay_data['version'])
        flash(len(replay_data['chat']))

        # Todo: get a unique replay id from storage, put some of replay_data in there
        replay_id = random.randint(1, 1000)

        # Todo: solid configurable data directories
        replay_path = os.path.join('perchweb', 'static', 'replays', f"{replay_id}.w3g")
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
