"""
Routes and views for the flask application.
"""

import os
from flask import Blueprint, url_for, request, redirect, flash, abort, current_app, send_file
from werkzeug.utils import secure_filename
from handler import standard_page
import replaydb
from filepaths import get_replay
from peep import get_max_id, get_pic, superlative
from auth import login as auth_login, check_if_admin
from perchlogging import log_to_slack, format_ip_addr
from templatefilters import lighten_color, url_slug
from lib.wigcodes import get_goldmines, get_neutral_buildings, get_starting_locations,\
                         get_map_size, get_mapinfo, get_map_creep_camps, \
                         get_map_canonical_name, player_colors

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
    """Redirect to slugged URL"""
    replay_listinfo = replaydb.get_replay_listinfo(replay_id, inc_views=True)
    replay_slug = url_slug(replay_listinfo['Name'])

    return redirect(url_for('views.view_replay_slug', replay_id=replay_id, replay_slug=replay_slug))


@routes.route('/replay/<int:replay_id>-<string:replay_slug>')
def view_replay_slug(replay_id, replay_slug):
    """Replay details"""

    replay_listinfo = replaydb.get_replay_listinfo(replay_id, inc_views=True)
    replay = replaydb.get_replay(replay_id)
    real_slug = url_slug(replay_listinfo['Name'])

    if replay_slug != real_slug:    # so we don't have badmanners making functioning links like /replay/123-unflattering-fake-text
        return redirect(url_for('views.view_replay_slug', replay_id=replay_id, replay_slug=real_slug))

    if replay_listinfo is None or replay is None:
        current_app.logger.warning(f'404 on replay view, ID: {replay_id}')
        abort(404)

    drawmap = replay.get_drawmap(timestamp=True, color_transform=lighten_color)
    game_count = replaydb.get_game_count(replay_id)
    return standard_page('replay.html', replay_listinfo['Name'], replay=replay, listinfo=replay_listinfo,
                         replay_id=replay_id, drawmap=drawmap, game_count=game_count,
                         next_id=replaydb.get_next_replay(replay_id), prev_id=replaydb.get_previous_replay(replay_id))


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


@routes.route('/map/<string:map_name>')
def view_map(map_name):
    """Map details"""
    canonical_name = get_map_canonical_name(map_name)
    if canonical_name:
        map_name = canonical_name

    map_stats = replaydb.get_map(map_name)

    if not map_stats:
        current_app.logger.warning(f'404 on map "{map_name}"')
        abort(404)

    recent_replays = replaydb.list_map_replays(map_name)
    # Todo: standardize drawmap
    goldmines = get_goldmines(map_name)
    map_size = get_map_size(map_name)
    neutral_buildings = get_neutral_buildings(map_name)
    start_locations = get_starting_locations(map_name, simple=False)
    creep_camps = get_map_creep_camps(map_name)

    # A lot of these calculations are really just reversing the SQL but it was faster to type here
    games = sum(gt['Games'] for gt in map_stats)
    map_info = {
        'name': map_name,
        'gold': sum(m['g'] for m in goldmines) if goldmines else None,
        'drawmap': {
            'map_size': map_size,
            'goldmines': [[m['x'], m['y'], m['g']] for m in goldmines] if goldmines else None,
            'neutralbuildings': [[b['x'], b['y'], b['id']] for b in neutral_buildings] if neutral_buildings else None,
            'starts': [[s['x'], s['y'], player_colors[int(s['player'])]] for s in start_locations] if start_locations else None,
            'creepcamps': creep_camps if creep_camps else None
        } if map_size else None,
        'games': games,
        'avg_length': sum(gt['AvgLength'] * gt['Games'] for gt in map_stats) // games,
        'avg_towers': sum(gt['AvgTowers'] * gt['Games'] for gt in map_stats) // games,
        'max_length': max(gt['AvgLength'] for gt in map_stats),
        'max_towers': max(gt['AvgTowers'] for gt in map_stats),
        'stats': map_stats,             # replay stats from database
        'info': get_mapinfo(map_name)   # map info from parsemaps
    }

    return standard_page('map.html', f'{map_name} details', map=map_info, recent_replays=recent_replays)


@routes.route('/maps')
def map_list():
    all_maps = replaydb.get_all_maps()
    maps_with_info = []
    for m in all_maps:
        info = get_mapinfo(m['name'])
        if info:
            m.update(info)
            maps_with_info.append(m)
    return standard_page('maps.html', 'Maps', maps=sorted(maps_with_info, key=lambda i: i['replay_count'], reverse=True))


@routes.route('/upload', methods=['POST'])
def upload_replay():
    """User replay uploads"""

    # Todo: Validation here, replay name, geoblocking etc
    replay_name = request.form['name'].strip()
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
    url = url_for('views.view_replay_slug',
                  replay_id=replay_id, replay_slug=url_slug(replay_name)) if replay_id is not None else url_for('views.index')
    return redirect(url)


@routes.route('/highperching')
def guide():
    """The art"""
    return standard_page('guide.html', 'The Art of Highperching', nav='guide')


@routes.route('/peep/', defaults={'pic_id': None})
@routes.route('/peep/<int:pic_id>')
def peep(pic_id):
    """Sometimes random pictures"""
    if (pic_id and pic_id > get_max_id()) or pic_id == 0:   # invalid pic ID
        return redirect(url_for('views.peep'))
    pic = get_pic(pic_id)
    replay_name = None
    if pic['replay_id']:
        replay_name = replaydb.get_replay_listinfo(pic['replay_id'])['Name']
    return standard_page('peep.html', 'Peep a pic', nav='peep', pic=pic,
                         perma=url_for('views.peep', pic_id=pic['id']),
                         replay_id=pic['replay_id'], replay_name=replay_name,
                         superlative=superlative)


@routes.route('/login', methods=['GET'])
def login_page():
    """ Admin login page, the only one admins can never see! """
    if check_if_admin(request.cookies):
        return redirect(url_for('views.index'))
    return standard_page('login.html', 'Log in', nav='admin')


@routes.route('/login', methods=['POST'])
def login_post():
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
    return redirect(url_for('views.login_page'))
