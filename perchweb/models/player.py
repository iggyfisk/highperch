""" Could do some data crunching here, count towers, calculate hero levels etc """
from copy import deepcopy
from lib.wigcodes import is_tower, tier_upgrades, item_codes


arbitrary_item_scores = {
    'stwp': -20,
    'tgrh': 15,
    'spre': 10,
    'ssan': 10,
    'mcri': 1,
    'bspd': 3,
    'stel': 4,
    'afac': 4,
    'ajen': 10,
    'kpin': 5,
    'lgdh': 10,
    'sdch': 4,
    'lhst': 4,
    'ward': 8,
}

arbitrary_building_scores = {
    'hvlt': 1,
    'ovln': 1,
    'emow': 1,
    'eden': 1,
    'utom': 1
}

official_names = {
    "iggythefisk#236",
    "Mata#2275",
    "Blinn#2885",
    "BEARAND#1604",
    "TIMG4STRok#1212",
    "IcebergSlim#145"
}


class Player(dict):
    """ Full replay player information, initialized from a replay data JSON file """

    def __init__(self, **args):
        super().__init__(**args)
        self.trades = [{'ms': t['ms'],
                        'outgoing': True if t['playerId'] == args['id'] else False,
                        'gold': t['gold'] if t['playerId'] == args['id'] else -t['gold'],
                        'lumber': t['lumber'] if t['playerId'] == args['id'] else -t['lumber']}
                       for t in self['tradeEvents']
                       if t['playerId'] == args['id'] or t['recipientPlayerId'] == args['id']]
        del self['tradeEvents']

    def official(self):
        """ Is this player an Officially Sanctioned player True/False """
        return self['name'] in official_names

    def tower_count(self):
        """ Total number of buildings made by this player that map to lib.wigcodes.is_tower """
        return sum(c for (i, c) in self['buildings']['summary'].items() if i in is_tower)

    def real_heroes(self):
        """ Filters out heroes from other races, used through shared control.
            This means levelups after player quit won't be captured,
            and doesn't detect shared heroes of the same race. Can be discussed."""
        # Screw you w3gjs and your partial 'E'->'N' renaming
        own_race = self['raceDetected'] if self['raceDetected'] != 'N' else 'E'
        return [h for h in self['heroes'] if h['id'][0] == 'N' or h['id'][0] == own_race]

    def net_feed(self):
        """ Net gold(0) and lumber(1) fed to allies this game """
        gold = 0
        lumber = 0
        for t in self.trades:
            gold += t['gold']
            lumber += t['lumber']
        return (gold, lumber)

    def first_share(self):
        """ Time until control shared with allies """
        return self['allyOptions'][0]['ms'] if len(self['allyOptions']) > 0 else None

    def towers_per_minute(self):
        stay_minutes = self['currentTimePlayed'] / 1000 / 60
        tpm = round((self.tower_count() / stay_minutes), 2)
        if tpm == 0:
            return None
        return tpm

    def get_action_types(self):
        action_types = deepcopy(self['actions'])
        action_types.pop('timed')
        return action_types

    def action_count(self):
        return sum(self.get_action_types().values())

    def get_arbitrary_score(self, ally_names):
        score = self['apm']
        score -= 40 if self['raceDetected'] == 'U' else 0

        heroes = self.real_heroes()
        score += len(heroes) * 30
        score += sum(h['level'] for h in heroes) * 2.5

        score += (self.tower_count() * 600000) / \
            (self['currentTimePlayed'] + 1)
        for (i, c) in self['buildings']['summary'].items():
            score += c * arbitrary_building_scores.get(i, 0)

        units = self['units']['summary']
        score += 15 if 'ngsp' in units else 0
        score += 10 if 'nzep' in units else 0

        items = self['items']['summary']
        score += 10 if 'rnec' in items else 0
        score += 10 if 'moon' in items else 0
        score += 15 if 'dust' in items else 0
        score += 10 if 'pinv' in items else 0
        for (i, c) in items.items():
            score += c * arbitrary_item_scores.get(i, 0)

        if self.official() and any(n in official_names for n in ally_names):
            first_share = self.first_share() or 3600000
            score -= (first_share - 45000) / 30000

        tier_ms = next((b['ms'] for b in self['buildings'].get(
            'order', []) if b['id'] in tier_upgrades), self['currentTimePlayed'])
        trade_score = 0
        for t in self.trades:
            scale = 0.002 / ((t['ms'] / 120000) + 0.5)
            scale += 0 if t['outgoing'] is False else (
                0 if tier_ms < t['ms'] else 0.001)
            trade_score += scale * 1.5 * t['gold']
            trade_score += scale * t['lumber']
        score += trade_score if trade_score > 0 else trade_score / 2

        return score

    def decode_items(self):
        player_race_shop = 'race_' + self['raceDetected']
        race_shops = ['race_H', 'race_O', 'race_N', 'race_U']
        race_shops.remove(player_race_shop)
        purchased_items = []
        for item_code, item_count in self['items']['summary'].items():
            try:
                item_name = item_codes[item_code]['name']
                item_cost = item_codes[item_code]['price'] * item_count
                item_shop = item_codes[item_code]['shop']
            except KeyError:
                item_name = item_code
                item_cost = 0
                item_shop = 'non-melee'
            item_priority = 6
            item_priority = 0 if item_shop == player_race_shop or item_shop == 'race_all' else item_priority
            item_priority = 1 if item_shop == 'ambiguous' else item_priority
            item_priority = 2 if item_shop == 'goblin' else item_priority
            item_priority = 3 if item_shop in race_shops else item_priority
            item_priority = 4 if item_shop == 'marketplace' else item_priority
            item_priority = 5 if item_shop == 'non-melee' else item_priority
            purchased_items.append({'name': item_name, 'count': item_count, 'gold': item_cost, 'priority': item_priority})
        return sorted(purchased_items, key=lambda i: i['priority'])

    def total_items_count(self):
        return sum(self['items']['summary'].values())

    def total_items_cost(self):
        total = 0
        for item_code, item_count in self['items']['summary'].items():
            total += item_codes[item_code]['price'] * item_count
        return total