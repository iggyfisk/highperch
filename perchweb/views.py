"""
Routes and views for the flask application.
"""

import os
from flask import Blueprint, url_for, request, redirect, flash, make_response
from werkzeug.utils import secure_filename
from handler import standard_page
import replaydb
from peep import get_pic
from admin import validate_admin_hash, check_if_admin

routes = Blueprint('views', __name__)


@routes.route('/')
def index():
    """Index, replay listing"""

    replay_filter = {
        'official': 'official' in request.args,
        'name': request.args.get('name', None),
        'map': request.args.get('map', None),
        'chat': request.args.get('chat', None),
        'sort': request.args.get('sort', 'id')
    }
    replays = replaydb.list_replays(replay_filter)

    # Testy thing
    if 'flash' in request.args:
        for i in range(int(request.args['flash'])):
            flash("Flash test string" * (i + 1))



    return standard_page('index.html', 'Replays', nav='index', replays=replays, replay_filter=replay_filter)


@routes.route('/replay/<int:replay_id>')
def view_replay(replay_id):
    """Replay details"""
    replay_listinfo = replaydb.get_replay_listinfo(replay_id, inc_views=True)
    replay = replaydb.get_replay(replay_id)

    if replay_listinfo is None or replay is None:
        # Todo: 404
        return redirect(url_for('views.index'))

    return standard_page('replay.html', replay_listinfo['Name'], replay=replay, listinfo=replay_listinfo, replay_id=replay_id)


@routes.route('/player/<string:battletag>')
def view_player(battletag):
    """Player details"""
    player = replaydb.get_player(battletag)

    if player is None:
        # Todo: 404
        return redirect(url_for('views.index'))

    recent_replays = replaydb.list_player_replays(battletag)

    player['name'] = battletag
    # Data crunching goes somewhere else later
    player['total_games'] = player['HUGames'] + \
        player['ORGames'] + player['NEGames'] + player['UDGames']

    return standard_page('player.html', f'{battletag} details', player=player, recent_replays=recent_replays)


@routes.route('/upload', methods=['POST'])
def upload_replay():
    """User replay uploads"""

    # Todo: Validation here, replay name, geoblocking etc
    replay_name = request.form['name']
    if (len(replay_name) < 6 or len(replay_name) > 50):
        flash('Bad name')
        return redirect(url_for('views.index'))

    # Proxy compatible? Might have to check X-Forwarded-For headers or similar
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

    replay_id = replaydb.save_replay(replay, replay_name, uploader_ip)
    url = url_for('views.view_replay',
                  replay_id=replay_id) if replay_id is not None else url_for('views.index')
    return redirect(url)


@routes.route('/highperching')
def guide():
    """The art"""
    return standard_page('guide.html', 'The Art of Highperching', nav='guide')


@routes.route('/peep/', defaults={'pic_id': None})
@routes.route('/peep/<int:pic_id>')
def peep(pic_id):
    """Sometimes random pictures"""
    pic = get_pic(pic_id)
    return standard_page('peep.html', 'Peep a pic', nav='peep', pic=pic,
                         perma=url_for('views.peep', pic_id=pic['id']))


@routes.route('/admin')
def admin():
    if check_if_admin(request.cookies):
        return redirect(url_for('views.index'))
    return standard_page('admin.html', 'Admin login', nav='admin')


@routes.route('/login', methods=['POST'])
def login():
    if validate_admin_hash(request.form['token']):
        flash('Welcome to the perch')
        response = make_response(redirect(url_for('views.admin')))
        response.set_cookie("HP_ADMIN_TOKEN", value=os.environ.get('HIGHPERCH_ADMIN_HASH'),
                            max_age=7305*86400, secure=True, httponly=True, samesite=True)
        return response
    else:
        flash('Invalid token')
        return redirect(url_for('views.admin'))
