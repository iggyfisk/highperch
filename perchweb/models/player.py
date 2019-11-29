""" Could do some data crunching here, count towers, calculate hero levels etc """

from lib.wigcodes import is_tower, tier_upgrades

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

# Todo: gather all the bnet tags
official_names = {
    "iggythefisk#236",
    "Mata#2275"
}


class Player(dict):
    """ Full player information, initialized from a replay data JSON file """

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
