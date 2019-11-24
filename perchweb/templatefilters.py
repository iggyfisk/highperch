""" Jinja2 utility filters """
from os.path import isfile, join
from re import compile as re_compile
from filepaths import get_path


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


thumbnails = {}
mapsize = re_compile('^\\(\\d\\)$')


def map_thumbnail(map_name):
    """ Map image src for a given map name, placeholder thumbnail if a real one can't be found """
    if map_name in thumbnails:
        return thumbnails[map_name]
    file_name = map_name[:-3] if map_name[-3:] == '_LV' else map_name
    file_name = file_name[3:] if mapsize.match(file_name[:3]) else file_name
    file_name = file_name.lower()
    if isfile(get_path(join('static', 'images', 'minimaps', f'{file_name}.jpg'))):
        thumbnails[map_name] = f'/static/images/minimaps/{file_name}.jpg'
    else:
        # Todo: real placeholder
        thumbnails[map_name] = f'/static/images/minimaps/fakethumbnail.jpg'
    return thumbnails[map_name]


tag_matcher = re_compile('^([^#]+)')


def player_display_name(player_name):
    """ Player name without # battle tag """
    match = tag_matcher.match(player_name)
    return match[0] if match else player_name


def register(jinja_environment):
    """ Register all filters to the given jinja environment """
    jinja_environment.filters['gametime'] = gametime
    jinja_environment.filters['chatmode'] = chatmode
    jinja_environment.filters['raceicon'] = race_icon
    jinja_environment.filters['racetitle'] = race_title
    jinja_environment.filters['mapthumbnail'] = map_thumbnail
    jinja_environment.filters['displayname'] = player_display_name
