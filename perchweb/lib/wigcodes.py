""" Warcraft 3 Game Data """

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

# Todo: Add manually as maps enter the rotation, or see if someone (wc3v?) has them standardized.
# Using Camera size from the world editor for now, seems to work
map_sizes = {
    '(8)Feralas_LV': {'minX': -8960, 'maxX': 8960, 'minY': -7424, 'maxY': 6912},
    '(6)Monsoon_LV': {'minX': -7680, 'maxX': 7680, 'minY': -8192, 'maxY': 7424},
    '(6)GnollWood': {'minX': -7424, 'maxX': 7936, 'minY': -8192, 'maxY': 7680},
    "(8)Mur'gulOasis_LV": {'minX': -7680, 'maxX': 7680, 'minY': -8192, 'maxY': 7680},
    "(8)TwilightRuins_LV": {'minX': -10496, 'maxX': 10496, 'minY': -11008, 'maxY': 10496},
    "(8)MarketSquare": {'minX': -8320, 'maxX': 8704, 'minY': -8576, 'maxY': 8960},
    '(6)RollingHills': {'minX': -3200, 'maxX': 3200, 'minY': -14720, 'maxY': 14208},
    '(2)TerenasStand_LV': {'minX': -4864, 'maxX': 4864, 'minY': -5376, 'maxY': 4864}
}
