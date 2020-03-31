""" API calls """

from flask import Blueprint, url_for, request, jsonify
from replaydb import list_replays

routes = Blueprint('api', __name__)

@routes.route('/search')
def search_replays():
    """ Replay listing """
    replay_filter = {
        'official': 'official' in request.args,
        'hasvod': 'hasvod' in request.args,
        'name': request.args.get('name', None),
        'map': request.args.get('map', None),
        'chat': request.args.get('chat', None),
        'sort': request.args.get('sort', 'id'),
        'player_name': request.args.get('player_name', None),
        'max_size': request.args.get('max_size', 100),
        'from': request.args.get('from', 0)
    }

    replays = list_replays(replay_filter)
    result = [{
        'name': r['Name'],
        'url': url_for('views.view_replay', replay_id=r['ID'], _external=True),
        'type': r['GameType'],
        'timestamp': r['TimeStamp'],
        'official': r['Official']
    } for r in replays]
    return jsonify(result)
