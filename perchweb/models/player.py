""" Could do some data crunching here, count towers, calculate hero levels etc """
class Player(dict):
    """ Full player information, initialized from a replay data JSON file """

    def tower_count(self):
        """ Todo: iterate over self['buildings']['summary'] and add all the tower types """
        return len(self['buildings']['summary'])
