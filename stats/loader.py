""" Lets us share some modules with the perchweb w/o import hell """
import os
import sys
from flask import Config
# Ugh I hate it
sys.path.append(os.path.realpath('perchweb'))

from replaydb import get_replay, get_all_replays
import filepaths as fp

config = Config('')
config.from_pyfile('perchweb/app.cfg')
fp.config = config
fp.script = True
