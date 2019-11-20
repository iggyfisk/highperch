""""
Initialize database schema, optionally create demo data
"""
import sqlite3

if __name__ == '__main__':
    wig_db = sqlite3.connect('wig.db')
    with open('test/wig.db.sql', mode='r') as f:
        wig_db.cursor().executescript(f.read())
    wig_db.commit()

    # Todo: integrate the StreamPoller
    # conn = sqlite3.connect('streams.db')
