""""
Run all existing replays through the parser again and update JSON+SQL
"""
import sys
import sqlite3
from os import path
from flask import Config
import perchweb.filepaths as fp

# Ugh I hate it
sys.path.append(path.realpath('perchweb'))
from perchweb.replaydb import reparse_replay


db = None


def get_connection():
    global db
    if db is None:
        db = sqlite3.connect(fp.get_db('wig.db'))
        db.row_factory = sqlite3.Row
    return db

def query(query_text, args=()):
    """ Run query_text with args against the stream db, one=True for a single result row """
    cursor = get_connection().execute(query_text, args)
    results = cursor.fetchall()
    cursor.close()
    return results

def commit():
    global db
    if db is not None:
        db.commit()
        db.close()

if __name__ == '__main__':
    if input("This re-create all JSON and DB data directly derived from replay parsing. Type 'yes' to continue: ") != 'yes':
        sys.exit(0)

    config = Config('')
    config.from_pyfile('perchweb/app.cfg')
    fp.config = config
    fp.script = True

    replays = query('SELECT ID FROM Replays')

    for r in replays:
        replay_id = r[0]
        print(f'Re-parsing replay with ID {replay_id}')
        reparse_replay(replay_id, query, fp)

    commit()