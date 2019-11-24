""" Jinja2 utility filters """


def gametime(milliseconds):
    """ Convert milliseconds to readable timestamp, like 34:04 """
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    return '{:01}:{:02}'.format(minutes, seconds)


chat_modes = {
    'ALL': 'All',
    'ALLY': 'Allies'
}


def chatmode(mode):
    """ Classic style chat mode """
    return chat_modes[mode]


def race_icon(race):
    """ Icon for single letter race ID """
    return f'/static/images/game/racesw3xp/{race}.gif'


race_titles = {
    'R': 'Random',
    'H': 'Human',
    'O': 'Orc',
    'N': 'Night Elf',
    'U': 'Noob Alert'
}
def race_title(race):
    """ Title text for single letter race ID """
    return race_titles[race]


def register(jinja_environment):
    """ Register all filters to the given jinja environment """
    jinja_environment.filters['gametime'] = gametime
    jinja_environment.filters['chatmode'] = chatmode
    jinja_environment.filters['raceicon'] = race_icon
    jinja_environment.filters['racetitle'] = race_title
