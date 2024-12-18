""" Could do some data crunching here, count towers, calculate hero levels etc """
from copy import deepcopy
from collections import defaultdict
from lib.wigcodes import is_tower, is_tower_upgrade, is_worker, tier_upgrades,\
    item_codes, unit_codes, building_codes, hero_names,\
    ability_codes, upgrade_codes, tinker_dupes


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
    'war2': 8
}

arbitrary_building_scores = {
    'hvlt': 1,
    'ovln': 1,
    'emow': 1,
    'eden': 1,
    'utom': 1
}

official_names = {
    "iggythefisk#236",  # legacy format clipping
    "iggythefisk#2369",
    "Mata#2275",
    "Blinn#2885",
    "BEARAND#1604",
    "TIMG4STRok#1212",
    "IcebergSlim#145",  # legacy format clipping
    "IcebergSlim#1452"
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
        self.real_apm = None

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
        try:
            return [h for h in self['heroes'] if h['id'][0] == 'N' or h['id'][0] == own_race]
        except KeyError:  # probably custom map
            return []

    def real_hero_ids(self):
        return [hero['id'] for hero in self.real_heroes()]

    def hero_abilities(self):
        # negotiable, this just fixes both cases in replayID 285. 155ms interval = 387apm
        skillup_lag_window_ms = 155
        heroes = {}
        for h in self['heroes']:
            if not 'id' in h or h['id'] not in hero_names:
                return {}  # probably custom map
            heroes[h['id']] = {}
            heroes[h['id']]['skills'] = defaultdict(int)
            heroes[h['id']]['retrains'] = 0
            heroes[h['id']]['level'] = 0
            last_skillup = ''
            last_skillup_ms = 0
            for a in h['abilityOrder']:
                if a['type'] == 'retraining':
                    heroes[h['id']]['retrains'] += 1
                    heroes[h['id']]['level'] = 0
                    heroes[h['id']]['skills'] = defaultdict(int)
                else:
                    # tinker ability IDs change with engineering upgrades
                    if a['value'] in tinker_dupes:
                        # set all occurrences of a tinker skill to the root skill ID
                        a['value'] = tinker_dupes[a['value']]
                    if a['time'] - last_skillup_ms <= skillup_lag_window_ms and a['value'] == last_skillup:
                        # they leveled up suspiciously fast, discard
                        continue
                    if heroes[h['id']]['skills'][a['value']] == 3:
                        # impossible (in melee) to skill past 3, discard
                        continue
                    if ability_codes[a['value']]['ult'] and heroes[h['id']]['skills'][a['value']] == 1:
                        # impossible (in melee) to multi-level ultimate, discard
                        continue
                    heroes[h['id']]['skills'][a['value']] += 1
                    heroes[h['id']]['level'] += 1
                    last_skillup = a['value']
                last_skillup_ms = a['time']

        return heroes

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

    def minutes_stayed(self):
        minutes = round(self['currentTimePlayed'] / 1000 / 60)
        return minutes if minutes else 1

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

    def get_feed_actions(self):
        actions = 0
        for t in self.trades:
            if t['outgoing']:
                actions += 2    # open and close the ally window
                for source in ['gold', 'lumber']:
                    if t[source] >= 200:
                        actions += (t[source] // 200) + 1 # conservatively assume use of control key
                    elif t[source] > 100:
                        actions += 2
                    else:
                        actions += 1
        return actions

    def action_count(self):
        game_actions = sum(self.get_action_types().values())
        return game_actions + self.get_feed_actions()

    def feed_action_ratio(self):
        if self.get_feed_actions() == 0 or self.action_count() == 0:
            return 0
        return self.get_feed_actions() / self.action_count()

    def get_real_apm(self):
        """ Use currentTimePlayed to calculate total APM instead of replay length.
            We can go back to using the parser output if w3gjs fixes this upstream
            Todo: update the output of replaydb.save_game_played() so that player
            APMs in database reflect this change """
        if self.real_apm is not None:
            return self.real_apm
        if self.action_count() == 0:
            self.real_apm = 0
        else:
            self.real_apm = round(
                (self.action_count() / (self['currentTimePlayed'] / 1000 / 60)))
        return self.real_apm

    def get_arbitrary_score(self, ally_names):
        score = self.get_real_apm()
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
        if player_race_shop in race_shops:  # catches 0-action players and maybe some edge cases
            race_shops.remove(player_race_shop)
        purchased_items = []
        for item_code, item_count in self['items']['summary'].items():
            if item_code in item_codes:
                item_name = item_codes[item_code]['name']
                item_cost = item_codes[item_code]['price'] * item_count
                item_shop = item_codes[item_code]['shop']
            else:
                item_name = item_code
                item_cost = 0
                item_shop = 'non-melee'
            # the idea is to show the items in ascending order of interesting, with marketplace last
            item_priority = 6
            item_priority = 0 if item_shop == player_race_shop or item_shop == 'race_all' else item_priority
            item_priority = 1 if item_shop == 'ambiguous' else item_priority
            item_priority = 2 if item_shop == 'goblin' else item_priority
            item_priority = 3 if item_shop in race_shops else item_priority
            item_priority = 4 if item_shop == 'marketplace' else item_priority
            item_priority = 5 if item_shop == 'non-melee' else item_priority
            purchased_items.append(
                {'name': item_name, 'count': item_count, 'gold': item_cost, 'priority': item_priority})
        return sorted(purchased_items, key=lambda i: i['priority'])

    def total_items_count(self):
        return sum(self['items']['summary'].values())

    def total_items_cost(self):
        total = 0
        for item_code, item_count in self['items']['summary'].items():
            total += item_codes[item_code]['price'] * item_count
        return total

    shopping_tables = ['perm_L3', 'perm_L4', 'perm_L5', 'perm_L6', 'artifact_L7',
                       'artifact_L8', 'charged_L4', 'charged_L5', 'charged_L6']

    def shopping_score(self):
        score = 0
        for item_code, item_count in self['items']['summary'].items():
            if item_codes[item_code]['table'] in self.shopping_tables:
                score += item_codes[item_code]['price'] * item_count
        return score

    def tp_count(self):
        tps = 0
        for item_code, item_count in self['items']['summary'].items():
            if item_code == 'stwp':
                tps += item_count
        return tps

    def decode_units(self):
        races = ['H', 'O', 'N', 'U']
        if self['raceDetected'] in races:
            races.remove(self['raceDetected'])
        created_units = []
        if 'hrtt' in self['units']['summary']:  # Siege Engine dedupe
            if 'hmtt' in self['units']['summary']:
                self['units']['summary']['hmtt'] += self['units']['summary']['hrtt']
                del self['units']['summary']['hrtt']
            else:
                self['units']['summary']['hmtt'] = self['units']['summary']['hrtt']
                del self['units']['summary']['hrtt']
        for unit_code, unit_count in self['units']['summary'].items():
            if unit_code in building_codes:
                continue  # it's a building upgrade
            if unit_code in unit_codes:
                unit_name = unit_codes[unit_code]['name']
                unit_gold = unit_codes[unit_code]['gold'] * unit_count
                unit_wood = unit_codes[unit_code]['wood'] * unit_count
                unit_race = unit_codes[unit_code]['race']
            else:
                unit_name = unit_code
                unit_gold, unit_wood = 0, 0
            unit_priority = 5
            unit_priority = 0 if unit_race == self['raceDetected'] else unit_priority
            unit_priority = 1 if unit_race == 'L' else unit_priority  # goblin lab
            unit_priority = 2 if unit_race == 'M' else unit_priority  # merc camp
            # leaver teammates, or, rarely, cool games
            unit_priority = 3 if unit_race in races else unit_priority
            created_units.append({'name': unit_name, 'count': unit_count,
                                  'gold': unit_gold, 'wood': unit_wood, 'priority': unit_priority})
        return sorted(created_units, key=lambda i: i['priority'])

    def total_units_count(self):
        units = 0
        for unit_code, unit_count in self['units']['summary'].items():
            if unit_code in unit_codes:
                units += unit_count
        return units

    def total_units_cost(self):
        gold = 0
        wood = 0
        for unit_code, unit_count in self['units']['summary'].items():
            if unit_code in building_codes:
                continue
            gold += unit_codes[unit_code]['gold'] * unit_count
            wood += unit_codes[unit_code]['wood'] * unit_count
        return (gold, wood)

    # Todo: something fun with this vs. army count. Ratio?
    def worker_units_count(self):
        worker_units = 0
        for unit_code, unit_count in self['units']['summary'].items():
            worker_units += unit_count if unit_code in is_worker else 0
        return worker_units

    # Todo: award for win with army count of zero with some "non-AFK" qualifiers
    def total_army_units(self):
        army_units = 0
        for unit_code, unit_count in self['items']['summary'].items():
            army_units += unit_count if unit_code not in is_worker and unit_code in unit_codes else 0
        return army_units

    def parse_building_code(self, code, count, races):
        if code in building_codes:
            building_name = building_codes[code]['name']
            building_gold = building_codes[code]['gold'] * count
            building_wood = building_codes[code]['wood'] * count
            building_race = building_codes[code]['race']
            building_tier = building_codes[code]['tier']
        elif code in tier_upgrades:
            building_name = unit_codes[code]['name']
            building_gold = unit_codes[code]['gold'] * count
            building_wood = unit_codes[code]['wood'] * count
            building_race = unit_codes[code]['race']
            building_tier = unit_codes[code]['tier']
        else:
            building_name = code
            building_gold = 0
            building_wood = 0
            building_race = 'neutral'
            building_tier = 1
        building_priority = 15
        building_priority = 1 if building_race == self['raceDetected'] else building_priority
        building_priority = 10 if building_race in races else building_priority
        building_priority += (1 +
                              building_tier) if code in tier_upgrades else 0
        building_priority -= 2 if code in is_tower else 0
        building_priority -= 1 if code in is_tower_upgrade else 0
        building_priority += (building_tier - 1)
        return {'name': building_name, 'count': count, 'gold': building_gold, 'wood': building_wood, 'race': building_race, 'tier': building_tier, 'priority': building_priority}

    def decode_buildings(self):
        races = ['H', 'O', 'N', 'U']
        if self['raceDetected'] in races:
            races.remove(self['raceDetected'])
        created_buildings = []
        for building_code, building_count in self['buildings']['summary'].items():
            created_buildings.append(self.parse_building_code(
                building_code, building_count, races))
        for unit_code, unit_count in self['units']['summary'].items():
            if unit_code in tier_upgrades or unit_code in is_tower_upgrade:
                created_buildings.append(
                    self.parse_building_code(unit_code, unit_count, races))
        return sorted(created_buildings, key=lambda i: i['priority'])

    def total_buildings_count(self):
        buildings = 0
        for building_code, building_count in self['buildings']['summary'].items():
            if building_code in building_codes:
                buildings += building_count
            if building_code in unit_codes:
                buildings += building_count
        return buildings

    def total_buildings_cost(self):
        gold = 0
        wood = 0
        for building_code, building_count in self['buildings']['summary'].items():
            if building_code in building_codes:
                gold += building_codes[building_code]['gold'] * building_count
                wood += building_codes[building_code]['wood'] * building_count
        return (gold, wood)

    def parse_actions(self):
        actions = self.get_action_types()
        actions['Assign group'] = actions.pop('assigngroup')
        actions['Right click'] = actions.pop('rightclick')
        actions['Misc. action'] = actions.pop('basic')
        actions['Build/train/purchase'] = actions.pop('buildtrain')
        actions['Use ability'] = actions.pop('ability')
        actions['Item give/drop'] = actions.pop('item')
        actions['Select'] = actions.pop('select')
        actions['Remove unit'] = actions.pop('removeunit')
        actions['Subgroup select'] = actions.pop('subgroup')
        actions['Select group'] = actions.pop('selecthotkey')
        actions['Esc'] = actions.pop('esc')
        actions['Minimap ping'] = actions.pop('ping')
        actions['Resource trade'] = self.get_feed_actions()
        nonzero_actions = {action: count for action,
                           count in actions.items() if count > 0}
        return list(nonzero_actions.items())

    def build_order(self):
        built = []

        last_build_id = ''
        last_build_ms = 0
        build_lag_window_ms = 155

        if len(self['units']['order']) > 0:
            for unit in self['units']['order']:
                if unit['id'] in building_codes:    # building upgrades are in the units array
                    if unit['id'] == last_build_id and unit['ms'] - last_build_ms <= build_lag_window_ms * 2:
                        continue
                    built.append(
                        {'type': 'building', 'id': unit['id'],
                         'name': building_codes[unit['id']]['name'], 'ms': unit['ms']})
                else:
                    built.append({'type': 'unit', 'id': unit['id'],
                                  'name': unit_codes[unit['id']]['name'], 'ms': unit['ms']})
                last_build_id = unit['id']
                last_build_ms = unit['ms']

        if 'order' in self['buildings']:
            [built.append({'type': 'building', 'id': building['id'], 'name': building_codes[building['id']]
                           ['name'], 'ms': building['ms']}) for building in self['buildings']['order']]

        upgrade_level = defaultdict(int)

        if len(self['upgrades']['order']) > 0:
            for upgrade in self['upgrades']['order']:
                if upgrade['id'] == last_build_id and upgrade['ms'] - last_build_ms <= build_lag_window_ms:
                    continue    # lag click
                if (upgrade_level[upgrade['id']] + 1) > len(upgrade_codes[upgrade['id']]['levels']):
                    continue    # impossible upgrade, probably due to previous cancelation or lag click
                built.append({'type': 'upgrade', 'id': upgrade['id'],
                              'name': upgrade_codes[upgrade['id']]['levels'][upgrade_level[upgrade['id']]]['name'],
                              'ms': upgrade['ms']})
                upgrade_level[upgrade['id']] += 1
                last_build_id = upgrade['id']
                last_build_ms = upgrade['ms']

        if len(self['items']['order']) > 0:
            [built.append({'type': 'item', 'id': item['id'], 'name': item_codes[item['id']]
                           ['name'], 'ms': item['ms']}) for item in self['items']['order']]

        if len(self['heroes']) > 0:
            for hero in self['heroes']:
                if not 'id' in hero or hero['id'] not in hero_names:
                    continue    # non-melee hero from custom map
                for ability in hero['abilityOrder']:
                    if ability['type'] == 'retraining':
                        built.append({'type': 'skillup', 'id': 'tret', 'name': 'Retrain Hero',
                                      'ms': ability['time']})
                        continue
                    if ability['value'] == last_build_id and ability['time'] - last_build_ms <= build_lag_window_ms:
                        continue    # lag click
                    built.append({'type': 'skillup', 'id': ability['value'],
                                  'name': ability_codes[ability['value']]['name'],
                                  'ms': ability['time']})
                    last_build_id = ability['value']
                    last_build_ms = ability['time']

        return sorted(built, key=lambda i: i['ms'])
