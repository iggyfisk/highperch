""""
Clear created content, initialize database schema, optionally create demo content
"""
import sys
import os
import glob
import shutil
import sqlite3
from flask import Config
import perchweb.filepaths as fp

if __name__ == '__main__':
    if input("This will delete all uploaded content and start fresh. Type 'yes' to continue: ") != 'yes':
        sys.exit(0)
    
    if os.path.isfile('perchweb/app.cfg'):
        if input("Type 'yes' to reset config: ") == 'yes':
            shutil.copyfile('test/dev.cfg', 'perchweb/app.cfg')
    else:
        shutil.copyfile('test/dev.cfg', 'perchweb/app.cfg')

    config = Config('')
    config.from_pyfile('perchweb/app.cfg')
    fp.config = config
    fp.script = True

    if os.path.isfile(fp.get_db('wig.db')):
        os.remove(fp.get_db('wig.db'))
    if os.path.isfile(fp.get_db('streams.db')):
        os.remove(fp.get_db('streams.db'))
    for data_file in glob.glob(fp.get_replay_data('*.json')):
        os.remove(data_file)
    for replay_file in glob.glob(fp.get_replay('*.w3g')):
        os.remove(replay_file)
    for peep_file in glob.glob(fp.get_peep('*')):
        if 'README.md' in peep_file:
            continue
        os.remove(peep_file)

    wig_db = sqlite3.connect(fp.get_db('wig.db'))
    with open('test/wig.db.sql', mode='r') as f:
        wig_db.cursor().executescript(f.read())
    wig_db.commit()

    stream_db = sqlite3.connect(fp.get_db('streams.db'))
    with open('test/streams.db.sql', mode='r') as f:
        stream_db.cursor().executescript(f.read())
    stream_db.commit()

    if input("Insert demo content? Type 'yes' to continue: ") == 'yes':
        shutil.copyfile('test/Reforged1.w3g', fp.get_replay('1.w3g'))
        shutil.copyfile('test/Reforged1.json', fp.get_replay_data('1.json'))
        shutil.copyfile('test/Reforged2.w3g', fp.get_replay('2.w3g'))
        shutil.copyfile('test/Reforged2.json', fp.get_replay_data('2.json'))
        shutil.copyfile('test/Reforged3.w3g', fp.get_replay('3.w3g'))
        shutil.copyfile('test/Reforged3.json', fp.get_replay_data('3.json'))
        shutil.copyfile('test/Reforged4.w3g', fp.get_replay('4.w3g'))
        shutil.copyfile('test/Reforged4.json', fp.get_replay_data('4.json'))
        shutil.copyfile('test/5.w3g', fp.get_replay('5.w3g'))
        shutil.copyfile('test/5.json', fp.get_replay_data('5.json'))
        shutil.copyfile('test/6.w3g', fp.get_replay('6.w3g'))
        shutil.copyfile('test/6.json', fp.get_replay_data('6.json'))
        shutil.copyfile('test/7.w3g', fp.get_replay('7.w3g'))
        shutil.copyfile('test/7.json', fp.get_replay_data('7.json'))
        shutil.copyfile('test/8.w3g', fp.get_replay('8.w3g'))
        shutil.copyfile('test/8.json', fp.get_replay_data('8.json'))
        for peep_file in glob.glob('test/peep/*'):
            shutil.copyfile(peep_file, fp.get_peep(os.path.basename(peep_file)))
        with open('test/wig.db.data.sql', mode='r') as f:
            wig_db.cursor().executescript(f.read())
        wig_db.commit()
    elif input("Insert production content? Type 'yes' to continue: ") == 'yes':
        for peep_file in glob.glob('test/peep/*'):
            shutil.copyfile(peep_file, fp.get_peep(os.path.basename(peep_file)))
        with open('test/wig.db.data.production.sql', mode='r') as f:
            wig_db.cursor().executescript(f.read())
        wig_db.commit()
