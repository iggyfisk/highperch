""" Warcraft 3 Game Data """
from filepaths import get_path
import json

race_titles = {
    'R': 'Random',
    'H': 'Human',
    'O': 'Orc',
    'N': 'Night Elf',  # Yes w3gjs remaps E to N for the different race fields
    'U': 'Noob Alert'
}

# Let's discuss capitalization
hero_names = {
    "Edem": "Demon Hunter",
    "Ekee": "Keeper of the Grove",
    "Emoo": "Priestess of the Moon",
    "Ewar": "Warden",
    "Hamg": "Archmage",
    "Hblm": "Blood Mage",
    "Hmkg": "Mountain King",
    "Hpal": "Paladin",
    "Nalc": "Goblin Alchemist",
    "Nbrn": "Dark Ranger",
    "Nbst": "Beastmaster",
    "Nfir": "Firelord",
    "Nngs": "Naga Sea Witch",
    "Npbm": "Pandaren Brewmaster",
    "Nplh": "Pit Lord",
    "Ntin": "Tinker",
    "Obla": "Blademaster",
    "Ofar": "Farseer",
    "Oshd": "Shadow Hunter",
    "Otch": "Tauren Chieftain",
    "Ucrl": "Crypt Lord",
    "Udea": "Death Knight",
    "Udre": "Dread Lord",
    "Ulic": "Lich"
}


is_tower = {'hwtw', 'owtw', 'etrp'}

tier_upgrades = {
    'hkee',
    'hcas',
    'ostr',
    'ofrt',
    'etoa',
    'etoe',
    'unp1',
    'unp2'
}


# Todo: move to a models/map when we create the map details

map_info = None


def get_map_size(map_name):
    global map_info
    if map_info is None:
        with open(get_path('resource/mapinfo.json'), 'r') as f:
            map_info = json.load(f)

    if map_name not in map_info:
        return None
    x = map_info[map_name]['x']
    y = map_info[map_name]['y']
    return [x[0], x[1], y[0], y[1]]


def get_starting_locations(map_name):
    global map_info
    if map_info is None:
        with open(get_path('resource/mapinfo.json'), 'r') as f:
            map_info = json.load(f)
    if map_name not in map_info:
        return None
    return map_info[map_name]['start']
