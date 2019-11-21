""" Get proper paths based on current flask app config """

from os import path
from flask import current_app

config = None
script = False

def cfg():
    return config or current_app.config

def get_path(p):
    if path.isabs(p):
        return p
    if script:
        return path.normpath(path.join('perchweb/', p))
    
    return path.normpath(path.join(current_app.root_path, p))

def get_db(filename):
    return get_path(path.join(cfg()['DB_PATH'], filename))

def get_replay_data(filename):
    return get_path(path.join(cfg()['REPLAY_DATA_PATH'], filename))

def get_replay(filename):
    return get_path(path.join(cfg()['REPLAY_PATH'], filename))

def get_temp(filename):
    return get_path(path.join(cfg()['TEMP_PATH'], filename))