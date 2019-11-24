""" Could do some data crunching here, count towers, calculate hero levels etc
    Methods or properties on init, who's to say. Inheritance, maybe I'm too RAD"""

import os
import json
from collections import defaultdict
from datetime import datetime
from models.player import Player

# Todo: gather all the bnet tags
official_names = {
    "iggpig#123",
    "ploter#2"
}


class ReplayListInfo(dict):
    """ Replay list information and partial data, initialized from a row in wig_db """

    def __init__(self, **args):
        super().__init__(**args)
        self['Players'] = json.loads(
            args['Players']) if 'Players' in args else None
        self['Chat'] = json.loads(args['Chat']) if 'Chat' in args else None

    def teams(self):
        """ Lists players separated by teams """
        teams = defaultdict(list)
        for p in self['Players']:
            teams[p['teamid']].append(p)
        return teams

    def upload_date(self):
        """ Replay upload timestamp as Python datetime """
        return datetime.fromtimestamp(self['TimeStamp'])


class Replay(dict):
    """ Full replay data, initialized from a replay data JSON file """

    def __init__(self, **args):
        super().__init__(**args)
        self.players = [Player(p) for p in args['players']]
        del self['players']
        self.player_colors = {p['id']: p['color'] for p in self.players}

    def teams(self):
        """ Lists players separated by teams """
        teams = defaultdict(list)
        for p in self.players:
            teams[p['teamid']].append(p)
        return teams

    def tower_count(self):
        """ Count every tower built by every player in this game """
        return sum(p.tower_count() for p in self.players)

    def map_name(self):
        """ More presentable map name """
        return os.path.splitext(os.path.basename(self['map']['file']))[0]

    def replay_saver(self):
        """ Returns the player that saved this replay """
        for p in self.players:
            if p['id'] == self['saverPlayerId']:
                return p
        return None

    def official(self):
        """ Returns True if an officially sanctioned replay else False """
        # Todo: check if any name in self.players in official_names
        return len(self.players) > 6
