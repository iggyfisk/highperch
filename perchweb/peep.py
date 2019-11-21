""" Peep a pic logic """

import random
from perchweb.replaydb import query_wig_db

random.seed()


def get_pic(pic_id=None):
    """ Returns a pic for peeping, random if no pic_id is specified """

    if pic_id is None:
        max_id_row = query_wig_db(
            'SELECT ID FROM Pics ORDER BY ID DESC LIMIT 1', one=True)
        max_id = (max_id_row or [1])[0]
        pic_id = random.randint(1, max_id)

    row = query_wig_db(
        'SELECT ID, ReplayID, Filename FROM Pics WHERE ID >= ? ORDER BY ID LIMIT 1', (pic_id,), one=True)
    pic = {'id': row['ID'],
           'replay_id': row['ReplayID'],
           'url': f'/static/images/peep/{row["FileName"]}'} if row is not None else None
    return (pic or {'id': 0, 'replay_id': None, 'url': '/'})
