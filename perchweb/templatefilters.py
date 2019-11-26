""" Jinja2 utility filters """
from os.path import isfile, join
from re import compile as re_compile
from filepaths import get_path
from lib.colors import lighten, scale
from lib.wigcodes import race_titles, hero_names
from admin import geoip_country
from urllib.parse import unquote


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


def race_title(race):
    """ Title text for single letter race ID """
    return race_titles[race]


def hero_name(hero_id):
    """ Translates a 4 letter hero ID to glorious full name """
    return hero_names[hero_id]


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


lightened_colors = {}


def lighten_color(hex_color, amount=0.07):
    """ Increases the light of a hex color by a factor of 0-1.0 """
    key = (hex_color, amount)
    if key not in lightened_colors:
        lightened_colors[key] = lighten(hex_color, amount)
    return lightened_colors[key]


scaled_colors = {}


def scale_color(hex_color, amount):
    """ Scales the light of a hex color by a factor of 0-1.0 """
    key = (hex_color, amount)
    if key not in scaled_colors:
        scaled_colors[key] = scale(hex_color, amount)
    return scaled_colors[key]


def make_country_embed(ip_addr):
    country = geoip_country(ip_addr)
    return f"<img src='/static/images/flags/{country['code'].lower()}.png' title='{country['name']}' class='countryflag'>"


def register(jinja_environment):
    """ Register all filters to the given jinja environment """
    jinja_environment.filters['gametime'] = gametime
    jinja_environment.filters['chatmode'] = chatmode
    jinja_environment.filters['raceicon'] = race_icon
    jinja_environment.filters['heroname'] = hero_name
    jinja_environment.filters['racetitle'] = race_title
    jinja_environment.filters['mapthumbnail'] = map_thumbnail
    jinja_environment.filters['displayname'] = player_display_name
    jinja_environment.filters['lighten'] = lighten_color
    jinja_environment.filters['scale'] = scale_color
    jinja_environment.filters['embed_country'] = make_country_embed
