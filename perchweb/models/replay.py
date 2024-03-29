""" Could do some data crunching here, count towers, calculate hero levels etc
    Methods or properties on init, who's to say. Inheritance, maybe I'm too RAD"""

import os
import json
from collections import defaultdict
from datetime import datetime
from math import sqrt
from templatefilters import lighten_color
from lib.wigcodes import is_tower, get_map_size, get_starting_locations,\
                         get_goldmines, ally_event_codes, get_map_canonical_name
from models.player import Player


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

    def upload_date_for_computers(self):
        return datetime.fromtimestamp(self['TimeStamp']).strftime("%Y-%m-%dT%H:%M:%S")

    def get_drawmap(self, color_transform=lambda c: c):
        """ Map size coordinates and a list of towers per color and coordinate,
            for drawing on the minimap. """
        map_size = get_map_size(get_map_canonical_name(self['Map']))
        recolored_start_locations = json.dumps({color_transform(color): coords for (
            color, coords) in json.loads(self['StartLocations']).items()})
        recolored_towers = json.dumps({color_transform(color): coords for (
            color, coords) in json.loads(self['Towers']).items()})
        return {'map_size': map_size, 'towers_json': recolored_towers, 'start_locations_json': recolored_start_locations}


class Replay(dict):
    """ Full replay data, initialized from a replay data JSON file """

    def __init__(self, **args):
        super().__init__(**args)
        # I'd like to turn all these cache values into @cached_property but that's Python >= 3.8
        self.arbitrary_scores = None
        self.formatted_chat = None
        self.chat_actions = None
        self.teams_dict = None
        self.arranged_teams = None

        self.players = [Player(tradeEvents=args['tradeEvents'], **p)
                        for p in self['players']]
        del self['players']
        # Need something more general
        self.player_colors = defaultdict(
            lambda: '#FFFFFF', {p['id']: p['color'] for p in self.players})
        self.player_names = {p['id']: p['name'] for p in self.players}

    def teams(self):
        """ Lists players separated by teams """
        if self.teams_dict is None:
            self.teams_dict = defaultdict(list)
            for p in self.players:
                self.teams_dict[p['teamid']].append(p)
        return self.teams_dict

    def tower_count(self):
        """ Count every tower built by every player in this game """
        return sum(p.tower_count() for p in self.players)

    def item_count(self):
        return sum(p.total_items_count() for p in self.players)

    def team_item_count(self, teamid):
        items = 0
        for p in self.players:
            if p['teamid'] == teamid:
                items += p.total_items_count()
        return items

    def team_item_cost(self, teamid):
        cost = 0
        for p in self.players:
            if p['teamid'] == teamid:
                cost += p.total_items_cost()
        return cost

    def team_unit_count(self, teamid):
        units = 0
        for p in self.players:
            if p['teamid'] == teamid:
                units += p.total_units_count()
        return units

    def team_unit_cost(self, teamid):
        gold = 0
        wood = 0
        for p in self.players:
            if p['teamid'] == teamid:
                gold += p.total_units_cost()[0]
                wood += p.total_units_cost()[1]
        return (gold, wood)

    def team_building_count(self, teamid):
        buildings = 0
        for p in self.players:
            if p['teamid'] == teamid:
                buildings += p.total_buildings_count()
        return buildings

    def team_building_cost(self, teamid):
        gold = 0
        wood = 0
        for p in self.players:
            if p['teamid'] == teamid:
                gold += p.total_buildings_cost()[0]
                wood += p.total_buildings_cost()[1]
        return (gold, wood)

    def map_name(self, fp=None):
        """ More presentable map name """
        return get_map_canonical_name(os.path.splitext(os.path.basename(self['map']['file']))[0], fp=fp)

    def replay_saver(self):
        """ Returns the player that saved this replay """
        if self['saverPlayerId'] == -1: # Saver unknown, very rare edge case
            return {'id': self['saverPlayerId'], 'name': 'Unknown#0'}
        for p in self.players:
            if p['id'] == self['saverPlayerId']:
                return p
        return None

    def official(self):
        """ Returns True if an officially sanctioned replay else False """
        saver = self.replay_saver()
        if saver['id'] == -1:   # Saver unknown, very rare edge case
            return False
        return saver.official() if saver is not None else False

    def get_arbitrary_scores(self):
        if not self.arbitrary_scores:
            self.arbitrary_scores = sorted(
                ((p['id'], p.get_arbitrary_score([a['name'] for a in self.teams()[p['teamid']] if a['id'] != p['id']]))
                 for p in self.players), key=lambda p: p[1])
        return self.arbitrary_scores

    def mvp_id(self):
        return self.get_arbitrary_scores()[-1][0]

    def grb_id(self):
        return self.get_arbitrary_scores()[0][0]

    # Minimum time between events to insert a space in the chatlog
    silence_period = 120000

    def get_chat_actions(self):
        if self.chat_actions is not None:
            return self.chat_actions
        chat_actions = {}
        for p in self.players:
            chat_actions[p['id']] = 0
        for chat in self['chat']:
            try:
                chat_actions[chat['playerId']] += (len(chat['message']) + 2)
            except KeyError: # probably a desync message from "Blizzard" with a nonexistent playerId
                pass
        self.chat_actions = chat_actions
        return self.chat_actions

    def loudest_player_id(self):
        top_id = sorted(self.get_chat_actions(),
                        key=self.get_chat_actions().get, reverse=True)[0]
        if self.get_chat_actions()[top_id] > 256:
            return top_id
        else:
            return None

    def most_ping_player_id(self):
        # Todo: maybe make this dependent on gamelength/player ingame time instead of absolute ping count
        ping_counts = {p['id']: p['actions']['ping'] for p in self.players}
        played_minutes = {p['id']: p.minutes_stayed() for p in self.players}
        top_id = sorted(ping_counts.items(),
                        key=lambda i: i[1], reverse=True)[0][0]
        if ping_counts[top_id] / played_minutes[top_id] > 2:    # arbitrary
            return top_id
        else:
            return None

    def best_shopper_player_id(self):
        shopping_scores = {p['id']: p.shopping_score() for p in self.players}
        top_id = sorted(shopping_scores.items(),
                        key=lambda i: i[1], reverse=True)[0][0]
        if shopping_scores[top_id] > 3000:
            return top_id
        else:
            return None

    def best_feeder_player_id(self):
        feed_percents = {p['id']: p.feed_action_ratio() for p in self.players}
        feed_actions = {p['id']: p.get_feed_actions() for p in self.players}
        top_id = sorted(feed_percents.items(),
                        key=lambda i: i[1], reverse=True)[0][0]
        if feed_percents[top_id] > 0.04 and feed_actions[top_id] > 100:
            return top_id
        else:
            return None

    def get_nohero_players(self):
        if self['duration'] < 480000 or self.game_host_type() != 'ladder':  # real games only
            return {p['id']: False for p in self.players}
        nohero = {p['id']: True for p in self.players}
        for p in self.players:
            if p['teamid'] != self['winningTeamId'] or \
               p.real_heroes() != [] or \
               p['currentTimePlayed'] / self['duration'] < 0.75 or \
               p.get_real_apm() < 50:
                nohero[p['id']] = False
        return nohero

    def game_host_type(self):
        if self['gamename'] == "BNet" and self['creator'] == "Battle.net" and self['privateString'] == '':
            return "ladder"
        elif self['privateString'] == 'hunter2': # this might change? someday?
            return "private"
        else:
            return "custom"

    def get_apm_data(self):
        apm_data = []
        final_minute = len(self.players[0]['actions']['timed'])
        for minute in range(len(self.players[0]['actions']['timed'])):
            apm_data.append({'minute': minute + 1})

        for p in self.players:
            leave_event = next((leave for leave in self['leaveEvents'] if leave['playerId'] == p['id']), None)
            if leave_event:
                leave_minute = int((leave_event['ms'] / 1000) // 60)
            else:
                leave_minute = len(self.players[0]['actions']['timed'])
            for minute, actions in enumerate(p['actions']['timed']):
                apm_mult = 1
                if leave_event and minute + 1 == final_minute and ((leave_event['ms']) // 1000) % 60:
                    apm_mult = 60 // ((leave_event['ms'] // 1000) % 60)
                if minute <= leave_minute:
                    apm_data[minute][p['name']] = actions * apm_mult

        return json.dumps(apm_data)

    def get_color_codes(self):
        return json.dumps([lighten_color(p['color']) for p in self.players])

    def get_ally_events(self):
        """ This only works accurately on changes to the shared control flag.
            Changes to shared vision and alliance aren't fully handled.
            We could be more precise about specific bitwise changes,
            but since only changes to shared control occur in ladder games I haven't bothered.
            I think the groupby performed here will also inaccurately collapse opposite
            state changes performed in the same gametick, e.g. changing from
            Ally A unshared/Ally B shared to the inverse in one shot.
            See lib/wigcodes.py for the breakdown of implemented flags"""
        ally_events = []

        for p in self.players:
            player_events = {}
            for event in p['allyOptions']:
                if 'playerId' in event:     # some custom games have targetless flags changes?
                    if not event['ms'] in player_events:
                        player_events[event['ms']] = {
                            'playerId': p['id'],
                            'recipientPlayerId': [event['playerId']],
                            'event': ally_event_codes[event['flags']],
                        }
                    else:
                        player_events[event['ms']]['recipientPlayerId'].append(event['playerId'])

            for event in player_events:
                merged_event = player_events[event]
                merged_event['ms'] = event
                ally_events.append(merged_event)

        return ally_events

    def get_team_size(self, player_id):
        team_id = next(p['teamid'] for p in self.players if p['id'] == player_id)
        size = next((len(self.teams()[team]) for team in self.teams() if team == team_id), None)
        return size

    earlygame_share_window = 600    # Cutoff for share-based AT detection (in seconds)

    def detect_arranged_teams(self):
        if self.arranged_teams is None:
            early_events = [e for e in self.get_ally_events() if e['ms'] < Replay.earlygame_share_window * 1000]
            mutual_shares = []
            for p in self.players:
                for e in early_events:
                    if e['playerId'] == p['id']:
                        for e2 in early_events:
                            if p['id'] in e2['recipientPlayerId']:
                                share_pair = sorted([e['playerId'], e2['playerId']])
                                if not share_pair in mutual_shares:
                                    mutual_shares.append(share_pair)
            # I took the below from https://stackoverflow.com/questions/4842613/merge-lists-that-share-common-elements
            if len(mutual_shares) > 0:
                team_groups = [mutual_shares[0]]
                for share in mutual_shares:
                    share_set = set(share)
                    merged = False
                    for index in range(len(team_groups)):
                        team_set = set(team_groups[index])
                        if len(share_set & team_set) != 0:
                            team_groups[index] = list(share_set | team_set)
                            merged = True
                            break
                    if not merged:
                        team_groups.append(share)
                arranged_teams = {}
                for team in team_groups:
                    arranged_teams[len(arranged_teams)] = team
                self.arranged_teams = arranged_teams

        return self.arranged_teams

    def get_arranged_team(self, playerId):
        arranged_teams = self.detect_arranged_teams()
        if arranged_teams:
            for team in arranged_teams:
                if playerId in arranged_teams[team]:
                    return team
        return None

    def get_formatted_chat(self):
        """ Chatlog, pause, resume, player left, and markers for periods of silence (indicated by None)"""
        if self.formatted_chat is not None:
            return self.formatted_chat

        merged_chat = self['chat'] + \
            [l for l in self['leaveEvents'] if l['reason'] != 'gameEnd'] + \
            self['pauseEvents'] + self['tradeEvents'] + self.get_ally_events()
        merged_chat.sort(key=lambda c: c['ms'])

        formatted_chat = []
        last_message_ms = 0
        for c in merged_chat:
            ms = c['ms']
            if 'reason' in c:
                c['leave'] = True

            if (last_message_ms > 0 and (ms - last_message_ms) > Replay.silence_period and
                ('message' in c or 'leave' in c or 'pause' in c)):
                formatted_chat.append(None)
                last_message_ms = ms

            c['mode'] = 'ALL' if 'mode' not in c else c['mode']
            if 'event' in c:
                c['mode'] = 'ALLY'
            c['player'] = self.player_names[c['playerId']
                                            ] if 'player' not in c else c['player']

            formatted_chat.append(c)
            if 'message' in c:
                last_message_ms = ms

        self.formatted_chat = formatted_chat
        return self.formatted_chat

    @staticmethod
    def pyth_distance(x0, x1, y0, y1):
        """ Distance between 2 2d points, wow """
        return sqrt(((x0 - x1)**2) + ((y0 - y1)**2))

    def get_drawmap(self, force=False, timestamp=False, color_transform=lambda c: c, fp=None):
        """ Map size coordinates and a list of towers per color and coordinate,
            for drawing on the minimap """

        canonical_name = self.map_name(fp=fp)

        map_size = get_map_size(canonical_name, fp=fp)
        start_locations = get_starting_locations(canonical_name, fp=fp)
        goldmines = get_goldmines(canonical_name, fp=fp)
        towers = None
        # pings = None
        player_start_locations = {}

        if map_size is not None or force:
            towers = {color_transform(p['color']):
                      [([b['x'], b['y'], b['ms']] if timestamp else [b['x'], b['y']])
                       for b in p['buildings'].get('order', []) if b['id'] in is_tower]
                      for p in self.players}
            # pings = {color_transform(p['color']):
            #          [([ping['x'], ping['y'], ping['ms']])
            #           for ping in p['pings']]
            #          for p in self.players}
            # Todo: figure out how to depict pings in an unclumsy way

        if start_locations is not None:
            for p in self.players:
                buildings = p['buildings'].get('order', [])
                if len(buildings) < 1:
                    continue
                x = buildings[0]['x']
                y = buildings[0]['y']

                player_start_locations[
                    color_transform(self.player_colors[p['id']])] = sorted(start_locations,
                                                                           key=lambda l: Replay.pyth_distance(l[0], x, l[1], y))[0]

        if goldmines is not None:
            goldmines = [[m['x'], m['y']] for m in goldmines]

        return {'map_size': map_size, 'towers': towers, 'start_locations': player_start_locations, 'goldmines': goldmines}

    def is_dota(self):
        if 'dota' in self['map']['file'].lower():
            return True
        return False