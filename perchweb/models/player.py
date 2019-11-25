""" Could do some data crunching here, count towers, calculate hero levels etc """

arbitrary_item_scores = {
    'stwp': -20,
    'tgrh': 15,
    'spre': 10,
    'ssan': 10,
    'mcri': 1
}


class Player(dict):
    """ Full player information, initialized from a replay data JSON file """

    def tower_count(self):
        """ Todo: iterate over self['buildings']['summary'] and add all the tower types """
        return len(self['buildings']['summary'])

    def real_heroes(self):
        """ Filters out heroes from other races, used through shared control.
            This means levelups after player quit won't be captured,
            and doesn't detect shared heroes of the same race. Can be discussed."""
        # Screw you w3gjs and your partial 'E'->'N' renaming
        own_race = self['raceDetected'] if self['raceDetected'] != 'N' else 'E'
        return [h for h in self['heroes'] if h['id'][0] == 'N' or h['id'][0] == own_race]

    def get_arbitrary_score(self):
        score = self['apm']
        score -= 40 if self['raceDetected'] == 'U' else 0

        heroes = self.real_heroes()
        score += len(heroes) * 30
        score += sum(h['level'] for h in heroes) * 2

        score += (self.tower_count() * 500000) / self['currentTimePlayed']

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

        return score


