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
        # Need something more general
        self.player_colors = {p['id']: p['color'] for p in self.players}
        self.player_names = {p['id']: p['name'] for p in self.players}
        # I'd like to turn all these cache values into @cached_property but that's Python >= 3.8
        self.arbitrary_scores = None
        self.formatted_chat = None

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

    def get_arbitrary_scores(self):
        if not self.arbitrary_scores:
            self.arbitrary_scores = sorted(
                ((p['id'], p.get_arbitrary_score()) for p in self.players), key=lambda p: p[1])
        return self.arbitrary_scores

    def mvp_id(self):
        return self.get_arbitrary_scores()[-1][0]

    def grb_id(self):
        return self.get_arbitrary_scores()[0][0]

    # Minimum time between events to insert a space in the chatlog
    silence_period = 180000

    def get_formatted_chat(self):
        """ Chatlog + player exits and markers for periods of silence (indicated by None)
            Bit of a DRY offender but it's tricky to merge two lists like this."""
        if self.formatted_chat is not None:
            return self.formatted_chat

        formatted_chat = []
        leave_events = self['leaveEvents'].copy()
        last_message_ms = 0

        for c in self['chat']:
            # Check if anyone left the game before this message
            while len(leave_events) > 0 and leave_events[0]['ms'] < c['timeMS']:
                leave = leave_events.pop(0)
                ms = leave['ms']
                player_id = leave['playerId']
                if len(formatted_chat) > 0 and (ms - last_message_ms) > Replay.silence_period:
                    formatted_chat.append(None)

                formatted_chat.append({
                    'timeMS': ms,
                    'mode': 'ALL',
                    'playerId': player_id,
                    'player': self.player_names[player_id],
                    'leave': True
                })
                last_message_ms = ms

            ms = c['timeMS']
            if len(formatted_chat) > 0 and (ms - last_message_ms) > Replay.silence_period:
                formatted_chat.append(None)

            formatted_chat.append(c)
            last_message_ms = ms

        # Players left after all the chat is done
        for leave in leave_events:
            ms = leave['ms']
            player_id = leave['playerId']
            if len(formatted_chat) > 0 and (ms - last_message_ms) > Replay.silence_period:
                formatted_chat.append(None)

            formatted_chat.append({
                'timeMS': ms,
                'mode': 'ALL',
                'playerId': player_id,
                'player': self.player_names[player_id],
                'leave': True
            })
            last_message_ms = ms

        self.formatted_chat = formatted_chat
        return self.formatted_chat
