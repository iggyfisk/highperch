"""
Routes and views for the flask application.
"""

import os
from flask import Blueprint, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from handler import standard_page
from replaydb import list_replays, get_replay, get_replay_listinfo, save_replay
from peep import get_pic

routes = Blueprint('views', __name__)

@routes.route('/')
def index():
    """Index"""
    # Todo: filter from query
    replays = list_replays({})

    return standard_page('index.html', 'Replays', nav='index', replays=replays)

@routes.route('/replay/<int:replay_id>')
def view_replay(replay_id):
    """Replay details"""
    replay_listinfo = get_replay_listinfo(replay_id, inc_views=True)
    replay = get_replay(replay_id)
    
    if replay_listinfo is None or replay is None:
        # Todo: 404
        return redirect(url_for('views.index'))

    return standard_page('replay.html', replay_listinfo['Name'], replay=replay, listinfo=replay_listinfo)


@routes.route('/upload', methods=['POST'])
def upload_replay():
    """User replay uploads"""

    # Todo: Validation here, replay name, geoblocking etc
    replay_name = request.form['name']
    # Proxy compatible?
    uploader_ip = request.remote_addr

    replay = request.files['replay'] if 'replay' in request.files else None
    replay_filename = secure_filename(
        replay.filename) if replay is not None else None
    if not replay_filename:
        flash('No replay file selected')
        return redirect(url_for('views.index'))

    replay_filename_parts = os.path.splitext(replay_filename)
    if len(replay_filename_parts) < 2 or replay_filename_parts[1] != '.w3g':
        flash('Not a .w3g replay')
        return redirect(url_for('views.index'))

    # Todo: Validation here, filesize etc

    save_replay(replay, replay_filename, replay_filename_parts, replay_name, uploader_ip)
    return redirect(url_for('views.index'))


@routes.route('/highperching')
def guide():
    """The art"""
    return standard_page('guide.html', 'The Art of Highperching', nav='guide')


@routes.route('/peep/', defaults={'pic_id': None})
@routes.route('/peep/<int:pic_id>')
def peep(pic_id):
    """Sometimes random pictures"""
    pic = get_pic(pic_id)
    return standard_page('peep.html', 'Peep a pic', nav='peep',
                         pic=pic,
                         perma=url_for('views.peep', pic_id=pic['id']))
