""""
Clear created content, initialize database schema, optionally create demo content
"""
import sys
import os
import glob
import shutil
import sqlite3


if __name__ == '__main__':
    if input("This will delete all uploaded content and start fresh. Type 'yes' to continue: ") != 'yes':
        sys.exit(0)

    if os.path.isfile('wig.db'):
        os.remove('wig.db')
    for data_file in glob.glob('replaydata/*.json'):
        os.remove(data_file)
    for replay_file in glob.glob('perchweb/static/replays/*.w3g'):
        os.remove(replay_file)

    wig_db = sqlite3.connect('wig.db')
    with open('test/wig.db.sql', mode='r') as f:
        wig_db.cursor().executescript(f.read())
    wig_db.commit()

    if input("Insert demo content? Type 'yes' to continue: ") != 'yes':
        sys.exit(0)

    shutil.copyfile('test/Reforged1.w3g', 'perchweb/static/replays/1.w3g')
    shutil.copyfile('test/Reforged1.json', 'replaydata/1.json')
    shutil.copyfile('test/Reforged2.w3g', 'perchweb/static/replays/2.w3g')
    shutil.copyfile('test/Reforged2.json', 'replaydata/2.json')
    shutil.copyfile('test/Reforged3.w3g', 'perchweb/static/replays/3.w3g')
    shutil.copyfile('test/Reforged3.json', 'replaydata/3.json')
    shutil.copyfile('test/Reforged4.w3g', 'perchweb/static/replays/4.w3g')
    shutil.copyfile('test/Reforged4.json', 'replaydata/4.json')
    with open('test/wig.db.data.sql', mode='r') as f:
        wig_db.cursor().executescript(f.read())
    wig_db.commit()

    # Todo: integrate the StreamPoller
    # conn = sqlite3.connect('streams.db')
