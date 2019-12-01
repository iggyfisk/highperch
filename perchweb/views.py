"""
Routes and views for the flask application.
"""

import os
from flask import Blueprint, url_for, request, redirect, flash, abort, current_app, send_file
from werkzeug.utils import secure_filename
from handler import standard_page
import replaydb
from filepaths import get_replay
from peep import get_pic
from auth import login as auth_login, check_if_admin
from perchlogging import log_to_slack, format_ip_addr

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
    filter_active = any(v and v != 'id' for v in replay_filter.values())
    replays = replaydb.list_replays(replay_filter)

    return standard_page('index.html', 'Replays', nav='index', replays=replays, replay_filter=replay_filter, filter_active=filter_active)


@routes.route('/replay/<int:replay_id>')
def view_replay(replay_id):
    """Replay details"""
    replay_listinfo = replaydb.get_replay_listinfo(replay_id, inc_views=True)
    replay = replaydb.get_replay(replay_id)

    if replay_listinfo is None or replay is None:
        current_app.logger.warning(f'404 on replay view, ID: {replay_id}')
        abort(404)

    drawmap = replay.get_drawmap(timestamp=True)
    return standard_page('replay.html', replay_listinfo['Name'], replay=replay, listinfo=replay_listinfo, replay_id=replay_id, drawmap=drawmap)


@routes.route('/replay/<int:replay_id>/download')
def download_replay(replay_id):
    """Custom replay download"""
    # Todo: banlist here, return a different send_file

    replay_listinfo = replaydb.get_replay_listinfo(
        replay_id, inc_downloads=True)

    if replay_listinfo is None:
        current_app.logger.warning(f'404 on replay download, ID: {replay_id}')
        abort(404)

    filename = ''.join(
        c for c in replay_listinfo['Name'] if c.isalnum() or c == ' ').strip()
    return send_file(get_replay(f'{replay_id}.w3g'), attachment_filename=f'{filename}.w3g', as_attachment=True)


@routes.route('/player/<string:battletag>')
def view_player(battletag):
    """Player details"""
    player = replaydb.get_player(battletag)

    if player is None:
        current_app.logger.warning(f'404 on player "{battletag}"')
        abort(404)

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
        error_string = f'Attempted bad replay name length from {format_ip_addr(request.remote_addr)}: "{replay_name}"'
        log_to_slack('WARNING', error_string)
        current_app.logger.warning(error_string)
        return redirect(url_for('views.index'))

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
        error_string = f'Attempted bad filename from {format_ip_addr(request.remote_addr)}: "{replay_filename}"'
        log_to_slack('WARNING', error_string)
        current_app.logger.warning(error_string)
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
    """ Admin login page, the only one admins can never see! """
    if check_if_admin(request.cookies):
        return redirect(url_for('views.index'))
    return standard_page('admin.html', 'Admin login', nav='admin')


@routes.route('/login', methods=['POST'])
def login():
    """ Log in and redirect back to index, now as an authenticated admin """
    response = auth_login(request.form['token'], url_for('views.index'))
    if response:
        flash('Welcome, wig dad')
        error_string = f'Successful admin login from {format_ip_addr(request.remote_addr)}'
        current_app.logger.warning(error_string)
        return response

    error_string = f'Failed admin login from {format_ip_addr(request.remote_addr)}'
    log_to_slack('ERROR', error_string)
    current_app.logger.error(error_string)

    flash('Invalid token')
    return redirect(url_for('views.admin'))
