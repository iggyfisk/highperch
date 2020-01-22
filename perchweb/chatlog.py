"""
Random footer chatlog, displayed in layout.html
"""

import random
from replaydb import query, get_replay_listinfo

random.seed()


def add_chatlog():
    """ Add a random 'chatlog' attribute """
    # Could be faster with some tricks but let's start there
    max_id_row = query('SELECT ID FROM Chatlogs ORDER BY ID DESC LIMIT 1', one=True)
    max_id = (max_id_row or [1])[0]
    log_id = random.randint(1, max_id)

    replay_name = None

    row = query(
        'SELECT ChatText, ReplayID FROM Chatlogs WHERE ID >= ? ORDER BY ID LIMIT 1', (log_id,), one=True)

    if row['ReplayID']:
        replay_name = get_replay_listinfo(row['ReplayID'])['Name']

    log = {'text': row['ChatText'],
           'replay_id': row['ReplayID'],
           'replay_name': replay_name} if row is not None else None

    return {'chatlog': log}
