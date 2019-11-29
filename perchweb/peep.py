""" Peep a pic logic """

import os
import random
from flask import flash, g
from replaydb import query, context_rollback_key
from filepaths import get_temp, get_peep

random.seed()


def get_pic(pic_id=None):
    """ Returns a pic for peeping, random if no pic_id is specified """
    if pic_id is None:
        max_id_row = query(
            'SELECT ID FROM Pics ORDER BY ID DESC LIMIT 1', one=True)
        max_id = (max_id_row or [1])[0]
        pic_id = random.randint(1, max_id)

    row = query(
        'SELECT ID, ReplayID, Filename FROM Pics WHERE ID >= ? ORDER BY ID LIMIT 1', (pic_id,), one=True)
    pic = {'id': row['ID'],
           'replay_id': row['ReplayID'],
           'url': f'/static/images/peep/{row["FileName"]}'} if row is not None else None
    return (pic or {'id': 0, 'replay_id': None, 'url': '/'})


def save_pic(pic, filename, replay_id=None):
    """ Save a pic for future peeping, possibly connected to a replay """
    if replay_id is not None:
        replay_exists = query(
            'SELECT ID FROM Replays WHERE ID = ?', (replay_id,), one=True)
        if replay_exists is None:
            flash(f'Referenced replay ID {replay_id} does not exist')
            return None

    unique = int.from_bytes(os.urandom(2), 'little')
    filename = f'{unique}_{filename}'
    temp_pic_path = get_temp(filename)
    pic.save(temp_pic_path)

    # From here on out we need to clean up if anything goes wrong
    try:
        query('INSERT INTO Pics(FileName, ReplayID) VALUES(?, ?)',
              (filename, replay_id))
        pic_id = query('SELECT last_insert_rowid()', one=True)[0]
        pic_path = get_peep(filename)
        os.rename(temp_pic_path, pic_path)

        flash('Picture very much uploaded')
        return pic_id
    except Exception as e:
        # Todo: log error
        flash('Picture upload failed, error follows')
        flash(str(e))
        setattr(g, context_rollback_key, True)
    finally:
        if os.path.isfile(temp_pic_path):
            os.remove(temp_pic_path)
