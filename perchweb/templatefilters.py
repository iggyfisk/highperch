""" Jinja2 utility filters """
from os.path import isfile, join
from re import compile as re_compile
from re import sub as re_sub
from filepaths import get_path
from lib.colors import lighten, scale
from lib.wigcodes import race_titles, hero_names
import geoip
from urllib.parse import unquote
from slugify import slugify


def gametime(milliseconds):
    """ Convert milliseconds to readable timestamp, like 34:04 """
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    return '{:01}:{:02}'.format(minutes, seconds)


def gametime_for_computers(milliseconds):
    """ Converts milliseconds to ISO8601 duration: PTPT1H4M20S
    Carryover is permitted in the standard so we don't need to worry about >24H gametimes """
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    if minutes >= 60:
        hours, minutes = divmod((minutes), 60)
        return f'PT{hours}H{minutes}M{seconds}S'
    return f'PT{minutes}M{seconds}S'


chat_modes = {
    'ALL': 'All',
    'ALLY': 'Allies'
}


def chatmode(mode):
    """ Classic style chat mode """
    if mode[:7] == 'PRIVATE':
        return 'Private'
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
        thumbnails[map_name] = f'/static/images/minimaps/unknownmap.png'
    return thumbnails[map_name]


def map_biglink(map_name):
    return re_sub('minimaps', 'bigmaps', map_thumbnail(map_name))


tag_matcher = re_compile('^([^#]+)')


def player_display_name(player_name):
    """ Player name without # battle tag """
    match = tag_matcher.match(player_name)
    return match[0] if match else player_name


def thousands(amount):
    """ Big number go down """
    return f'{round(amount / 1000, 1)}k'


lightened_colors = {
    ('#0000FF', 0.05): '#2443f0',   # plain blue
    ('#008080', 0.05): '#3f9682',   # dark teal
    ('#3eb489', 0.05): '#6e6e6e',   # dark gray? or light teal/#79e0c8?
    ('#800080', 0.05): '#8b3fba',   # plain purple or dark purple?
    ('#FFFF00', 0.05): '#e8d227',   # plain yellow
    ('#FF0000', 0.05): '#db2323',   # plain red
    ('#FFC0CB', 0.05): '#ff91ca',   # plain pink?
    ('#000080', 0.05): '#0d0da3',   # dark blue
    ('#E6E6FA', 0.05): '#d6bae8'    # "light purple"
}


def lighten_color(hex_color, amount=0.05):
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
    country = geoip.lookup_country(ip_addr)
    return f"<img src='/static/images/flags/{country['code'].lower()}.png' title='{country['name']}' class='countryflag'>"


def url_slug(title):
    """ This will probably not end up living here. WIP """
    return slugify(title, replacements=[["'", '']])


def register(jinja_environment):
    """ Register all filters to the given jinja environment """
    jinja_environment.filters['gametime'] = gametime
    jinja_environment.filters['gametime_for_computers'] = gametime_for_computers
    jinja_environment.filters['chatmode'] = chatmode
    jinja_environment.filters['raceicon'] = race_icon
    jinja_environment.filters['heroname'] = hero_name
    jinja_environment.filters['racetitle'] = race_title
    jinja_environment.filters['mapthumbnail'] = map_thumbnail
    jinja_environment.filters['bigmapurl'] = map_biglink
    jinja_environment.filters['displayname'] = player_display_name
    jinja_environment.filters['lighten'] = lighten_color
    jinja_environment.filters['scale'] = scale_color
    jinja_environment.filters['embed_country'] = make_country_embed
    jinja_environment.filters['thousands'] = thousands
    jinja_environment.filters['slugify'] = url_slug
