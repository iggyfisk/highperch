"""
Random footer chatlog, displayed in layout.html
"""

import random

# Todo: SQLite storage, import from oldperch
chatlogs = [
    {'messages': [
        '(05:35 / All) BEAR_AND: u remember the map Highperch(6)?',
        '(05:38 / All) BEAR_AND: scotty',
        '(05:40 / All) Scotty_Potty: OMG',
        '(05:41 / All) Scotty_Potty: YOU@!',
        '(05:43 / All) Scotty_Potty: FUCK YOU',
        '(05:46 / All) O[r]Ks: lol',
        '(05:53 / All) Scotty_Potty: i remeber that so well',
        '(05:58 / All) Scotty_Potty: are u in clan towa'
    ]},
    {'messages': [
        '(102:05 / All) AndreasCarlson: *i slowly grasp ur belt and unbuckle it and slide my hand in ur pants.',
        '(102:24 / All) AndreasCarlson: *a voice in ur head tells u to go ahead, and u slowlyu open ur legs as i grab ur throbbing member*',
        '(102:34 / All) AndreasCarlson: * it warm i say i know u say*',
        '(102:44 / All) AndreasCarlson: i pull it on and i open my mouth and i gently suck on it',
        '(102:56 / All) AndreasCarlson: then u thrust and moan and i start grabbing u and kissing u like crazy',
        '(103:03 / All) AndreasCarlson: then i take my dick out and we jerk eachother off',
        '(103:16 / All) AndreasCarlson: i get close to climax and all of a sudden i release all over u',
        '(103:26 / All) AndreasCarlson: i aim for ur chest but some get in ur mouth and ur eyes and ur hair',
        '(103:34 / All) AndreasCarlson: then u lick my asshole as i suck u off',
        '(103:43 / All) AndreasCarlson: u explode in my mouth but i dont swallow',
        '(103:58 / All) AndreasCarlson: i get up and start making out with u, we keep swapping back and forth for what seme like eternity',
        '(104:07 / All) AndreasCarlson: we fall asleep with our dicks in each other hand'
    ]}
]
random.seed()


def add_chatlog():
    return {'chatlog': chatlogs[random.randint(0, len(chatlogs) - 1)]}
