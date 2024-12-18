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
    "Ofar": "Far Seer",
    "Oshd": "Shadow Hunter",
    "Otch": "Tauren Chieftain",
    "Ucrl": "Crypt Lord",
    "Udea": "Death Knight",
    "Udre": "Dread Lord",
    "Ulic": "Lich"
}

item_codes = {
    "stwp": {"name": "Scroll of Town Portal", "table": "shop", "shop": "ambiguous", "price": 350},
    "dust": {"name": "Dust of Appearance", "table": "shop", "shop": "ambiguous", "price": 75},
    "shea": {"name": "Scroll of Healing", "table": "shop", "shop": "ambiguous", "price": 250},

    "plcl": {"name": "Lesser Clarity Potion", "table": "shop", "shop": "race_all", "price": 70},
    "phea": {"name": "Potion of Healing", "table": "shop", "shop": "race_all", "price": 150},
    "pman": {"name": "Potion of Mana", "table": "shop", "shop": "race_all", "price": 200},

    "ofir": {"name": "Orb of Fire", "table": "shop", "shop": "race_H", "price": 325},
    "ofr2": {"name": "Orb of Fire", "table": "shop", "shop": "race_H", "price": 325},
    "tsct": {"name": "Ivory Tower", "table": "shop", "shop": "race_H", "price": 40},
    "mcri": {"name": "Mechanical Critter", "table": "shop", "shop": "race_H", "price": 50},
    "sreg": {"name": "Scroll of Regeneration", "table": "shop", "shop": "race_H", "price": 100},
    "ssan": {"name": "Staff of Sanctuary", "table": "shop", "shop": "race_H", "price": 250},

    "oli2": {"name": "Orb of Lightning", "table": "shop", "shop": "race_O", "price": 375},
    "hslv": {"name": "Healing Salve", "table": "shop", "shop": "race_O", "price": 100},
    "shas": {"name": "Scroll of Speed", "table": "shop", "shop": "race_O", "price": 50},
    "tgrh": {"name": "Tiny Great Hall", "table": "shop", "shop": "race_O", "price": 600},

    "oven": {"name": "Orb of Venom", "table": "shop", "shop": "race_N", "price": 325},
    "pams": {"name": "Anti-magic Potion", "table": "shop", "shop": "race_N", "price": 100},
    "moon": {"name": "Moonstone", "table": "shop", "shop": "race_N", "price": 50},
    "spre": {"name": "Staff of Preservation", "table": "shop", "shop": "race_N", "price": 150},

    "ocor": {"name": "Orb of Corruption", "table": "shop", "shop": "race_U", "price": 375},
    "ritd": {"name": "Ritual Dagger", "table": "shop", "shop": "race_U", "price": 125},
    "skul": {"name": "Sacrificial Skull", "table": "shop", "shop": "race_U", "price": 50},
    "rnec": {"name": "Rod of Necromancy", "table": "shop", "shop": "race_U", "price": 150},

    "bspd": {"name": "Boots of Speed", "table": "shop", "shop": "goblin", "price": 250},
    "prvt": {"name": "Periapt of Vitality", "table": "shop", "shop": "goblin", "price": 325},
    "pinv": {"name": "Potion of Invisibility", "table": "shop", "shop": "goblin", "price": 100},
    "spro": {"name": "Scroll of Protection", "table": "shop", "shop": "goblin", "price": 150},
    "cnob": {"name": "Circlet of Nobility", "table": "shop", "shop": "goblin", "price": 175},
    "pnvl": {"name": "Potion of Lesser Invulnerability", "table": "shop", "shop": "goblin", "price": 150},
    "stel": {"name": "Staff of Teleportation", "table": "shop", "shop": "goblin", "price": 150},
    "tret": {"name": "Tome of Retraining", "table": "shop", "shop": "goblin", "price": 300},

    "clsd": {"name": "Cloak of Shadows", "table": "perm_L1", "shop": "marketplace", "price": 100},
    "rst1": {"name": "Gauntlets of Ogre Strength +3", "table": "perm_L1", "shop": "marketplace", "price": 100},
    "rin1": {"name": "Mantle of Intelligence +3", "table": "perm_L1", "shop": "marketplace", "price": 100},
    "rag1": {"name": "Slippers of Agility +3", "table": "perm_L1", "shop": "marketplace", "price": 100},

    "rat6": {"name": "Claws of Attack +6", "table": "perm_L2", "shop": "marketplace", "price": 125},
    "gcel": {"name": "Gloves of Haste", "table": "perm_L2", "shop": "marketplace", "price": 125},
    "rde1": {"name": "Ring of Protection +2", "table": "perm_L2", "shop": "marketplace", "price": 125},
    "rde2": {"name": "Ring of Protection +3", "table": "perm_L2", "shop": "marketplace", "price": 125},

    "rat9": {"name": "Claws of Attack +9", "table": "perm_L3", "shop": "marketplace", "price": 300},
    "crys": {"name": "Crystal Ball", "table": "perm_L3", "shop": "marketplace", "price": 300},
    "penr": {"name": "Pendant of Energy", "table": "perm_L3", "shop": "marketplace", "price": 300},
    "rlif": {"name": "Ring of Regeneration", "table": "perm_L3", "shop": "marketplace", "price": 300},
    "evtl": {"name": "Talisman of Evasion", "table": "perm_L3", "shop": "marketplace", "price": 300},
    "rde3": {"name": "Ring of Protection +4", "table": "perm_L3", "shop": "marketplace", "price": 300},

    "belv": {"name": "Boots of Quel'Thalas +6", "table": "perm_L4", "shop": "marketplace", "price": 400},
    "ciri": {"name": "Robe of the Magi +6", "table": "perm_L4", "shop": "marketplace", "price": 400},
    "bgst": {"name": "Belt of Giant Strength +6", "table": "perm_L4", "shop": "marketplace", "price": 400},
    "afac": {"name": "Alleria's Flute of Accuracy", "table": "perm_L4", "shop": "marketplace", "price": 400},
    "brac": {"name": "Runed Bracers", "table": "perm_L4", "shop": "marketplace", "price": 400},
    "sbch": {"name": "Scourge Bone Chimes", "table": "perm_L4", "shop": "marketplace", "price": 400},
    "rwiz": {"name": "Sobi Mask", "table": "perm_L4", "shop": "marketplace", "price": 400},
    "lhst": {"name": "The Lion Horn of Stormwind", "table": "perm_L4", "shop": "marketplace", "price": 400},

    "ajen": {"name": "Ancient Janggo of Endurance", "table": "perm_L5", "shop": "marketplace", "price": 500},
    "ratc": {"name": "Claws of Attack +12", "table": "perm_L5", "shop": "marketplace", "price": 500},
    "clfm": {"name": "Cloak of Flames", "table": "perm_L5", "shop": "marketplace", "price": 500},
    "hval": {"name": "Helm of Valor", "table": "perm_L5", "shop": "marketplace", "price": 500},
    "hcun": {"name": "Hood of Cunning", "table": "perm_L5", "shop": "marketplace", "price": 500},
    "kpin": {"name": "Khadgar's Pipe of Insight", "table": "perm_L5", "shop": "marketplace", "price": 500},
    "lgdh": {"name": "Legion Doom-Horn", "table": "perm_L5", "shop": "marketplace", "price": 500},
    "mcou": {"name": "Medallion of Courage", "table": "perm_L5", "shop": "marketplace", "price": 500},
    "ward": {"name": "Warsong Battle Drums", "table": "perm_L5", "shop": "marketplace", "price": 500},
    "war2": {"name": "Warsong Battle Drums", "table": "perm_L5", "shop": "marketplace", "price": 500}, # when did this change?

    "spsh": {"name": "Amulet of Spell Shield", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "rhth": {"name": "Khadgar's Gem of Health", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "odef": {"name": "Orb of Darkness", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "pmna": {"name": "Pendant of Mana", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "rde4": {"name": "Ring of Protection +5", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "ssil": {"name": "Staff of Silence", "table": "perm_L6", "shop": "marketplace", "price": 600},

    "ratf": {"name": "Claws of Attack +15", "table": "artifact_L7", "shop": "marketplace", "price": 800},
    "desc": {"name": "Kelen's Dagger of Escape", "table": "artifact_L7", "shop": "marketplace", "price": 800},
    "ofro": {"name": "Orb of Frost", "table": "artifact_L7", "shop": "marketplace", "price": 800},
    "infs": {"name": "Inferno Stone", "table": "artifact_L7", "shop": "marketplace", "price": 800},

    "ckng": {"name": "Crown of Kings +5", "table": "artifact_L8", "shop": "marketplace", "price": 1000},
    "modt": {"name": "Mask of Death", "table": "artifact_L8", "shop": "marketplace", "price": 1000},
    "tkno": {"name": "Tome of Power", "table": "artifact_L8", "shop": "marketplace", "price": 1250},

    "rej3": {"name": "Replenishment Potion", "table": "charged_L2", "shop": "marketplace", "price": 150},
    "wswd": {"name": "Sentry Wards", "table": "charged_L2", "shop": "marketplace", "price": 150},
    "will": {"name": "Wand of Illusion", "table": "charged_L2", "shop": "marketplace", "price": 150},
    "wlsd": {"name": "Wand of Lightning Shield", "table": "charged_L2", "shop": "marketplace", "price": 150},

    "pghe": {"name": "Potion of Greater Healing", "table": "charged_L3", "shop": "marketplace", "price": 400},
    "pgma": {"name": "Potion of Greater Mana", "table": "charged_L3", "shop": "marketplace", "price": 400},
    "pnvu": {"name": "Potion of Invulnerability", "table": "charged_L3", "shop": "marketplace", "price": 400},
    "sror": {"name": "Scroll of the Beast", "table": "charged_L3", "shop": "marketplace", "price": 400},
    "woms": {"name": "Wand of Mana Stealing", "table": "charged_L3", "shop": "marketplace", "price": 400},

    "ankh": {"name": "Ankh of Reincarnation", "table": "charged_L4", "shop": "marketplace", "price": 450},
    "fgsk": {"name": "Book of the Dead", "table": "charged_L4", "shop": "marketplace", "price": 450},
    "whwd": {"name": "Healing Wards", "table": "charged_L4", "shop": "marketplace", "price": 450},
    "hlst": {"name": "Health Stone", "table": "charged_L4", "shop": "marketplace", "price": 450},
    "mnst": {"name": "Mana Stone", "table": "charged_L4", "shop": "marketplace", "price": 450},
    "wcyc": {"name": "Wand of the Wind", "table": "charged_L4", "shop": "marketplace", "price": 450},

    "pdiv": {"name": "Potion of Divinity", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "pres": {"name": "Potion of Restoration", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "fgrd": {"name": "Red Drake Egg", "table": "charged_L5", "shop": "marketplace", "price": 550},          # deprecated in 1.32.6
    "fgbd": {"name": "Blue Drake Egg", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "sres": {"name": "Scroll of Restoration", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "fgfh": {"name": "Spiked Collar", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "fgrg": {"name": "Stone Token", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "totw": {"name": "Talisman of the Wild", "table": "charged_L5", "shop": "marketplace", "price": 550},   # deprecated in 1.32.6
    "iotw": {"name": "Idol of the Wild", "table": "charged_L5", "shop": "marketplace", "price": 550},

    "wild": {"name": "Amulet of the Wild", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "fgdg": {"name": "Demonic Figurine", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "shar": {"name": "Ice Shard", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "ccmd": {"name": "Scepter of Mastery", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "scav": {"name": "Scepter of Avarice", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "engr": {"name": "Engraved Scale", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "sand": {"name": "Scroll of Animate Dead", "table": "charged_L6", "shop": "marketplace", "price": 700}, # deprecated in 1.32.6
    "srrc": {"name": "Scroll of Resurrection", "table": "charged_L6", "shop": "marketplace", "price": 700}, # deprecated in 1.32.6

    "amrc": {"name": "Amulet of Recall", "table": "non-melee", "shop": "non-melee", "price": 0},
    "ccmd": {"name": "Scepter of Mastery", "table": "non-melee", "shop": "non-melee", "price": 0},
    "gemt": {"name": "Gem of True Seeing", "table": "non-melee", "shop": "non-melee", "price": 0},
    "gobm": {"name": "Goblin Land Mines", "table": "non-melee", "shop": "non-melee", "price": 0},
    "gsou": {"name": "Soul Gem", "table": "non-melee", "shop": "non-melee", "price": 0},
    "guvi": {"name": "Glyph of Ultravision", "table": "non-melee", "shop": "non-melee", "price": 0},
    "gfor": {"name": "Glyph of Fortification", "table": "non-melee", "shop": "non-melee", "price": 0},
    "soul": {"name": "Soul", "table": "non-melee", "shop": "non-melee", "price": 0},
    "mdpb": {"name": "Medusa Pebble", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rat3": {"name": "Claws of Attack +3", "table": "non-melee", "shop": "non-melee", "price": 0},
    "olig": {"name": "Orb of Lightning", "table": "non-melee", "shop": "non-melee", "price": 0},
    "pgin": {"name": "Potion of Greater Invisibility", "table": "non-melee", "shop": "non-melee", "price": 0},
    "pspd": {"name": "Potion of Speed", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sfog": {"name": "Horn of the Clouds", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sman": {"name": "Scroll of Mana", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tels": {"name": "Goblin Night Scope", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tdex": {"name": "Tome of Agility", "table": "non-melee", "shop": "non-melee", "price": 0},
    "texp": {"name": "Tome of Experience", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tint": {"name": "Tome of Intelligence", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tstr": {"name": "Tome of Strength", "table": "non-melee", "shop": "non-melee", "price": 0},
    "wneg": {"name": "Wand of Negation", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rdis": {"name": "Rune of Dispel Magic", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rwat": {"name": "Rune of the Watcher", "table": "non-melee", "shop": "non-melee", "price": 0},
    "engs": {"name": "Enchanted Gemstone", "table": "non-melee", "shop": "non-melee", "price": 0},
    "k3m1": {"name": "Mooncrystal", "table": "non-melee", "shop": "non-melee", "price": 0},
    "nspi": {"name": "Necklace of Spell Immunity", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tgxp": {"name": "Tome of Greater Experience", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tpow": {"name": "Tome of Knowledge", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tst2": {"name": "Tome of Strength +2", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tin2": {"name": "Tome of Intelligence +2", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tdx2": {"name": "Tome of Agility +2", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rde0": {"name": "Ring of Protection +1", "table": "non-melee", "shop": "non-melee", "price": 0},
    "manh": {"name": "Manual of Health", "table": "non-melee", "shop": "non-melee", "price": 0},
    "phlt": {"name": "Phat Lewt", "table": "non-melee", "shop": "non-melee", "price": 0},
    "gopr": {"name": "Glyph of Purification", "table": "non-melee", "shop": "non-melee", "price": 0},
    "ches": {"name": "Cheese", "table": "non-melee", "shop": "non-melee", "price": 0},
    "mlst": {"name": "Maul of Strength", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rnsp": {"name": "Ring of Superiority", "table": "non-melee", "shop": "non-melee", "price": 0},
    "brag": {"name": "Bracer of Agility", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sksh": {"name": "Skull Shield", "table": "non-melee", "shop": "non-melee", "price": 0},
    "vddl": {"name": "Voodoo Doll", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sprn": {"name": "Spider Ring", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tmmt": {"name": "Totem of Might", "table": "non-melee", "shop": "non-melee", "price": 0},
    "anfg": {"name": "Ancient Figurine", "table": "non-melee", "shop": "non-melee", "price": 0},
    "lnrn": {"name": "Lion's Ring", "table": "non-melee", "shop": "non-melee", "price": 0},
    "iwbr": {"name": "Ironwood Branch", "table": "non-melee", "shop": "non-melee", "price": 0},
    "jdrn": {"name": "Jade Ring", "table": "non-melee", "shop": "non-melee", "price": 0},
    "drph": {"name": "Druid Pouch", "table": "non-melee", "shop": "non-melee", "price": 0},
    "pclr": {"name": "Clarity Potion", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rej1": {"name": "Minor Replenishment Potion", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rej2": {"name": "Lesser Replenishment Potion", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rej4": {"name": "Greater Replenishment Potion", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rej5": {"name": "Lesser Scroll of Replenishment ", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rej6": {"name": "Greater Scroll of Replenishment ", "table": "non-melee", "shop": "non-melee", "price": 0},
    "gold": {"name": "Gold Coins", "table": "non-melee", "shop": "non-melee", "price": 0},
    "lmbr": {"name": "Bundle of Lumber", "table": "non-melee", "shop": "non-melee", "price": 0},
    "fgun": {"name": "Flare Gun", "table": "non-melee", "shop": "non-melee", "price": 0},
    "pomn": {"name": "Potion of Omniscience", "table": "non-melee", "shop": "non-melee", "price": 0},
    "gomn": {"name": "Glyph of Omniscience", "table": "non-melee", "shop": "non-melee", "price": 0},
    "wneu": {"name": "Wand of Neutralization", "table": "non-melee", "shop": "non-melee", "price": 0},
    "silk": {"name": "Spider Silk Broach", "table": "non-melee", "shop": "non-melee", "price": 0},
    "lure": {"name": "Monster Lure", "table": "non-melee", "shop": "non-melee", "price": 0},
    "vamp": {"name": "Vampiric Potion", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tcas": {"name": "Tiny Castle", "table": "non-melee", "shop": "non-melee", "price": 0},
    "wshs": {"name": "Wand of Shadowsight", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sneg": {"name": "Staff of Negation", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sbok": {"name": "Spell Book", "table": "non-melee", "shop": "non-melee", "price": 0},
    "oslo": {"name": "Orb of Slow", "table": "non-melee", "shop": "non-melee", "price": 0},
    "dsum": {"name": "Diamond of Summoning", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sor1": {"name": "Shadow Orb +1", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sor2": {"name": "Shadow Orb +2", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sor3": {"name": "Shadow Orb +3", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sor4": {"name": "Shadow Orb +4", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sor5": {"name": "Shadow Orb +5", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sor6": {"name": "Shadow Orb +6", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sor7": {"name": "Shadow Orb +7", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sor8": {"name": "Shadow Orb +8", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sor9": {"name": "Shadow Orb +9", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sora": {"name": "Shadow Orb +10", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sorf": {"name": "Shadow Orb Fragment", "table": "non-melee", "shop": "non-melee", "price": 0},
    "fwss": {"name": "Frost Wyrm Skull Shield", "table": "non-melee", "shop": "non-melee", "price": 0},
    "ram1": {"name": "Ring of the Archmagi", "table": "non-melee", "shop": "non-melee", "price": 0},
    "ram2": {"name": "Ring of the Archmagi", "table": "non-melee", "shop": "non-melee", "price": 0},
    "ram3": {"name": "Ring of the Archmagi", "table": "non-melee", "shop": "non-melee", "price": 0},
    "ram4": {"name": "Ring of the Archmagi", "table": "non-melee", "shop": "non-melee", "price": 0},
    "shtm": {"name": "Shamanic Totem", "table": "non-melee", "shop": "non-melee", "price": 0},
    "shwd": {"name": "Shimmerweed", "table": "non-melee", "shop": "non-melee", "price": 0},
    "btst": {"name": "Battle Standard", "table": "non-melee", "shop": "non-melee", "price": 0},
    "skrt": {"name": "Skeletal Artifact", "table": "non-melee", "shop": "non-melee", "price": 0},
    "thle": {"name": "Thunder Lizard Egg", "table": "non-melee", "shop": "non-melee", "price": 0},
    "sclp": {"name": "Secret Level Powerup", "table": "non-melee", "shop": "non-melee", "price": 0},
    "gldo": {"name": "Orb of Kil'jaeden", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tbsm": {"name": "Tiny Blacksmith", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tfar": {"name": "Tiny Farm", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tlum": {"name": "Tiny Lumber Mill", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tbar": {"name": "Tiny Barracks", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tbak": {"name": "Tiny Altar of Kings", "table": "non-melee", "shop": "non-melee", "price": 0},
    "mgtk": {"name": "Magic Key Chain", "table": "non-melee", "shop": "non-melee", "price": 0},
    "stre": {"name": "Staff of Reanimation", "table": "non-melee", "shop": "non-melee", "price": 0},
    "horl": {"name": "Sacred Relic", "table": "non-melee", "shop": "non-melee", "price": 0},
    "hbth": {"name": "Helm of Battlethirst", "table": "non-melee", "shop": "non-melee", "price": 0},
    "blba": {"name": "Bladebane Armor", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rugt": {"name": "Runed Gauntlets", "table": "non-melee", "shop": "non-melee", "price": 0},
    "frhg": {"name": "Firehand Gauntlets", "table": "non-melee", "shop": "non-melee", "price": 0},
    "gvsm": {"name": "Gloves of Spell Mastery", "table": "non-melee", "shop": "non-melee", "price": 0},
    "crdt": {"name": "Crown of the Deathlord", "table": "non-melee", "shop": "non-melee", "price": 0},
    "arsc": {"name": "Arcane Scroll", "table": "non-melee", "shop": "non-melee", "price": 0},
    "scul": {"name": "Scroll of the Unholy Legion", "table": "non-melee", "shop": "non-melee", "price": 0},
    "tmsc": {"name": "Tome of Sacrifices", "table": "non-melee", "shop": "non-melee", "price": 0},
    "dtsb": {"name": "Drek'thar's Spellbook", "table": "non-melee", "shop": "non-melee", "price": 0},
    "grsl": {"name": "Grimoire of Souls", "table": "non-melee", "shop": "non-melee", "price": 0},
    "arsh": {"name": "Arcanite Shield", "table": "non-melee", "shop": "non-melee", "price": 0},
    "shdt": {"name": "Shield of the Deathlord", "table": "non-melee", "shop": "non-melee", "price": 0},
    "shhn": {"name": "Shield of Honor", "table": "non-melee", "shop": "non-melee", "price": 0},
    "shen": {"name": "Enchanted Shield", "table": "non-melee", "shop": "non-melee", "price": 0},
    "thdm": {"name": "Thunderlizard Diamond", "table": "non-melee", "shop": "non-melee", "price": 0},
    "stpg": {"name": "Clockwork Penguin", "table": "non-melee", "shop": "non-melee", "price": 0},
    "shrs": {"name": "Shimmerglaze Roast", "table": "non-melee", "shop": "non-melee", "price": 0},
    "bfhr": {"name": "Bloodfeather's Heart", "table": "non-melee", "shop": "non-melee", "price": 0},
    "cosl": {"name": "Celestial Orb of Souls", "table": "non-melee", "shop": "non-melee", "price": 0},
    "shcw": {"name": "Shaman Claws", "table": "non-melee", "shop": "non-melee", "price": 0},
    "srbd": {"name": "Searing Blade", "table": "non-melee", "shop": "non-melee", "price": 0},
    "frgd": {"name": "Frostguard", "table": "non-melee", "shop": "non-melee", "price": 0},
    "envl": {"name": "Enchanted Vial", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rump": {"name": "Rusty Mining Pick", "table": "non-melee", "shop": "non-melee", "price": 0},
    "mort": {"name": "Mogrin's Report", "table": "non-melee", "shop": "non-melee", "price": 0},
    "srtl": {"name": "Serathil", "table": "non-melee", "shop": "non-melee", "price": 0},
    "stwa": {"name": "Sturdy War Axe", "table": "non-melee", "shop": "non-melee", "price": 0},
    "klmm": {"name": "Killmaim", "table": "non-melee", "shop": "non-melee", "price": 0},
    "rots": {"name": "Scepter of the Sea", "table": "non-melee", "shop": "non-melee", "price": 0},
    "axas": {"name": "Ancestral Staff", "table": "non-melee", "shop": "non-melee", "price": 0},
    "mnsf": {"name": "Mindstaff", "table": "non-melee", "shop": "non-melee", "price": 0},
    "schl": {"name": "Scepter of Healing", "table": "non-melee", "shop": "non-melee", "price": 0},
    "asbl": {"name": "Assassin's Blade", "table": "non-melee", "shop": "non-melee", "price": 0},
    "kgal": {"name": "Keg of Ale", "table": "non-melee", "shop": "non-melee", "price": 0},
    "dphe": {"name": "Thunder Phoenix Egg", "table": "non-melee", "shop": "non-melee", "price": 0},
    "dkfw": {"name": "Keg of Thunderwater", "table": "non-melee", "shop": "non-melee", "price": 0},
    "dthb": {"name": "Thunderbloom Bulb", "table": "non-melee", "shop": "non-melee", "price": 0}
}

unit_codes = {
    "hfoo": {"name": 'Footman', "race": "H", "gold": 135, "wood": 0, "food": 2, "level": 2},
    "hkni": {"name": 'Knight', "race": "H", "gold": 245, "wood": 60, "food": 4, "level": 4},
    "hmpr": {"name": 'Priest', "race": "H", "gold": 135, "wood": 10, "food": 2, "level": 2},
    "hmtm": {"name": 'Mortar Team', "race": "H", "gold": 180, "wood": 70, "food": 3, "level": 2},
    "hpea": {"name": 'Peasant', "race": "H", "gold": 75, "wood": 0, "food": 1, "level": 1},
    "hrif": {"name": 'Rifleman', "race": "H", "gold": 205, "wood": 30, "food": 3, "level": 3},
    "hsor": {"name": 'Sorceress', "race": "H", "gold": 155, "wood": 20, "food": 2, "level": 2},
    "hmtt": {"name": 'Siege Engine', "race": "H", "gold": 195, "wood": 60, "food": 4, "level": 3},
    "hrtt": {"name": 'Siege Engine', "race": "H", "gold": 195, "wood": 60, "food": 4, "level": 3},
    "hgry": {"name": 'Gryphon Rider', "race": "H", "gold": 280, "wood": 70, "food": 4, "level": 5},
    "hgyr": {"name": 'Flying Machine', "race": "H", "gold": 100, "wood": 30, "food": 1, "level": 1},
    "hspt": {"name": 'Spell Breaker', "race": "H", "gold": 215, "wood": 30, "food": 3, "level": 3},
    "hdhw": {"name": 'Dragonhawk Rider', "race": "H", "gold": 200, "wood": 30, "food": 3, "level": 3},

    "ebal": {"name": 'Glaive Thrower', "race": "N", "gold": 210, "wood": 65, "food": 3, "level": 2},
    "echm": {"name": 'Chimaera', "race":  "N", "gold": 330, "wood": 70, "food": 5, "level": 5},
    "edoc": {"name": 'Druid of the Claw', "race": "N", "gold": 255, "wood": 80, "food": 4, "level": 4},
    "edot": {"name": 'Druid of the Talon', "race": "N", "gold": 145, "wood": 20, "food": 2, "level": 2},
    "ewsp": {"name": 'Wisp', "race": "N", "gold": 60, "wood": 0, "food": 1, "level": 1},
    "esen": {"name": 'Huntress', "race": "N", "gold": 195, "wood": 20, "food": 3, "level": 3},
    "earc": {"name": 'Archer', "race": "N", "gold": 130, "wood": 10, "food": 2, "level": 2},
    "edry": {"name": 'Dryad', "race": "N", "gold": 145, "wood": 60, "food": 3, "level": 3},
    "ehip": {"name": 'Hippogryph', "race": "N", "gold": 160, "wood": 20, "food": 2, "level": 2},
    "emtg": {"name": 'Mountain Giant', "race": "N", "gold": 350, "wood": 100, "food": 7, "level": 6},
    "efdr": {"name": 'Faerie Dragon', "race": "N", "gold": 155, "wood": 25, "food": 2, "level": 3},

    "ocat": {"name": 'Demolisher', "race": "O", "gold": 220, "wood": 50, "food": 4, "level": 2},
    "odoc": {"name": 'Troll Witch Doctor', "race": "O", "gold": 145, "wood": 25, "food": 2, "level": 2},
    "ogru": {"name": 'Grunt', "race": "O", "gold": 200, "wood": 0, "food": 3, "level": 3},
    "ohun": {"name": 'Troll Headhunter', "race": "O", "gold": 140, "wood": 20, "food": 2, "level": 2},
    "otbk": {"name": 'Troll Berserker', "race": "O", "gold": 140, "wood": 20, "food": 2, "level": 2},
    "okod": {"name": 'Kodo Beast', "race": "O", "gold": 255, "wood": 60, "food": 4, "level": 4},
    "opeo": {"name": 'Peon', "race": "O", "gold": 75, "wood": 0, "food": 1, "level": 1},
    "orai": {"name": 'Raider', "race": "O", "gold": 180, "wood": 40, "food": 3, "level": 3},
    "oshm": {"name": 'Shaman', "race": "O", "gold": 130, "wood": 20, "food": 2, "level": 2},
    "otau": {"name": 'Tauren', "race": "O", "gold": 280, "wood": 80, "food": 5, "level": 5},
    "owyv": {"name": 'Wind Rider', "race": "O", "gold": 265, "wood": 40, "food": 4, "level": 4},
    "ospw": {"name": 'Spirit Walker', "race": "O", "gold": 195, "wood": 35, "food": 3, "level": 3},
    "ospm": {"name": 'Spirit Walker', "race": "O", "gold": 195, "wood": 35, "food": 3, "level": 3},
    "otbr": {"name": 'Troll Batrider', "race": "O", "gold": 160, "wood": 40, "food": 2, "level": 2},

    "uaco": {"name": 'Acolyte', "race": "U", "gold": 75, "wood": 0, "food": 1, "level": 1},
    "uabo": {"name": 'Abomination', "race": "U", "gold": 240, "wood": 70, "food": 4, "level": 4},
    "uban": {"name": 'Banshee', "race": "U", "gold": 155, "wood": 30, "food": 2, "level": 2},
    "ucry": {"name": 'Crypt Fiend', "race": "U", "gold": 215, "wood": 40, "food": 3, "level": 3},
    "ufro": {"name": 'Frost Wyrm', "race": "U", "gold": 385, "wood": 120, "food": 7, "level": 6},
    "ugar": {"name": 'Gargoyle', "race": "U", "gold": 175, "wood": 30, "food": 2, "level": 2},
    "ugho": {"name": 'Ghoul', "race": "U", "gold": 120, "wood": 0, "food": 2, "level": 2},
    "unec": {"name": 'Necromancer', "race": "U", "gold": 145, "wood": 20, "food": 2, "level": 2},
    "umtw": {"name": 'Meat Wagon', "race": "U", "gold": 230, "wood": 50, "food": 4, "level": 2},
    "ushd": {"name": 'Shade', "race": "U", "gold": 0, "wood": 0, "food": 1, "level": 1},
    "uobs": {"name": 'Obsidian Statue', "race": "U", "gold": 200, "wood": 35, "food": 3, "level": 2},
    "ubsp": {"name": 'Destroyer', "race": "U", "gold": 300, "wood": 85, "food": 5, "level": 5},

    "nskm": {"name": 'Skeletal Marksman', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "nskf": {"name": 'Burning Archer', "race": "M", "gold": 225, "wood": 25, "food": 2, "level": 3},
    "nws1": {"name": 'Dragon Hawk', "race": "M", "gold": 350, "wood": 70, "food": 4, "level": 5},
    "nban": {"name": 'Bandit', "race": "M", "gold": 105, "wood": 0, "food": 1, "level": 1},
    "nrog": {"name": 'Rogue', "race": "M", "gold": 150, "wood": 0, "food": 2, "level": 3},
    "nenf": {"name": 'Enforcer', "race": "M", "gold": 215, "wood": 20, "food": 4, "level": 5},
    "nass": {"name": 'Assassin', "race": "M", "gold": 250, "wood": 30, "food": 3, "level": 4},
    "nbdk": {"name": 'Black Drake', "race": "M", "gold": 365, "wood": 80, "food": 5, "level": 6},
    "nrdk": {"name": 'Red Dragon Whelp', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "nbdr": {"name": 'Black Dragon Whelp', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "nrdr": {"name": 'Red Drake', "race": "M", "gold": 365, "wood": 80, "food": 5, "level": 6},
    "nbwm": {"name": 'Black Dragon', "race": "M", "gold": 745, "wood": 200, "food": 8, "level": 10},
    "nrwm": {"name": 'Red Dragon', "race": "M", "gold": 745, "wood": 200, "food": 8, "level": 10},
    "nadr": {"name": 'Blue Dragon', "race": "M", "gold": 745, "wood": 200, "food": 8, "level": 10},
    "nadw": {"name": 'Blue Dragon Whelp', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "nadk": {"name": 'Blue Drake', "race": "M", "gold": 365, "wood": 80, "food": 5, "level": 6},
    "nbzd": {"name": 'Bronze Dragon', "race": "M", "gold": 745, "wood": 200, "food": 8, "level": 10},
    "nbzk": {"name": 'Bronze Drake', "race": "M", "gold": 365, "wood": 80, "food": 5, "level": 6},
    "nbzw": {"name": 'Bronze Dragon Whelp', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "ngrd": {"name": 'Green Dragon', "race": "M", "gold": 745, "wood": 200, "food": 8, "level": 10},
    "ngdk": {"name": 'Green Drake', "race": "M", "gold": 365, "wood": 80, "food": 5, "level": 6},
    "ngrw": {"name": 'Green Dragon Whelp', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "ncea": {"name": 'Centaur Archer', "race": "M", "gold": 150, "wood": 10, "food": 2, "level": 2},
    "ncen": {"name": 'Centaur Outrunner', "race": "M", "gold": 195, "wood": 0, "food": 3, "level": 4},
    "ncer": {"name": 'Centaur Drudge', "race": "M", "gold": 150, "wood": 10, "food": 2, "level": 2},
    "ndth": {"name": 'Dark Troll High Priest', "race": "M", "gold": 255, "wood": 30, "food": 3, "level": 4},
    "ndtp": {"name": 'Dark Troll Shadow Priest', "race": "M", "gold": 195, "wood": 10, "food": 2, "level": 2},
    "ndtb": {"name": 'Dark Troll Berserker', "race": "M", "gold": 255, "wood": 30, "food": 3, "level": 4},
    "ndtw": {"name": 'Dark Troll Warlord', "race": "M", "gold": 365, "wood": 80, "food": 5, "level": 6},
    "ndtr": {"name": 'Dark Troll', "race": "M", "gold": 150, "wood": 10, "food": 2, "level": 2},
    "ndtt": {"name": 'Dark Troll Trapper', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "nfsh": {"name": 'Forest Troll High Priest', "race": "M", "gold": 305, "wood": 40, "food": 4, "level": 4},
    "nfsp": {"name": 'Forest Troll Shadow Priest', "race": "M", "gold": 195, "wood": 10, "food": 2, "level": 2},
    "nftr": {"name": 'Forest Troll', "race": "M", "gold": 150, "wood": 10, "food": 2, "level": 2},
    "nftb": {"name": 'Forest Troll Berserker', "race": "M", "gold": 245, "wood": 30, "food": 3, "level": 4},
    "nftt": {"name": 'Forest Troll Trapper', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "nftk": {"name": 'Forest Troll Warlord', "race": "M", "gold": 365, "wood": 80, "food": 5, "level": 6},
    "ngrk": {"name": 'Mud Golem', "race": "M", "gold": 145, "wood": 10, "food": 2, "level": 2},
    "ngir": {"name": 'Goblin Shredder', "race": "L", "gold": 375, "wood": 100, "food": 4, "level": 4},
    "nfrs": {"name": 'Furbolg Shaman', "race": "M", "gold": 255, "wood": 30, "food": 3, "level": 4},
    "ngna": {"name": 'Gnoll Poacher', "race": "M", "gold": 105, "wood": 0, "food": 1, "level": 1},
    "ngns": {"name": 'Gnoll Assassin', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "ngno": {"name": 'Gnoll', "race": "M", "gold": 105, "wood": 0, "food": 1, "level": 1},
    "ngnb": {"name": 'Gnoll Brute', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "ngnw": {"name": 'Gnoll Warden', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "ngnv": {"name": 'Gnoll Overseer', "race": "M", "gold": 305, "wood": 35, "food": 4, "level": 5},
    "ngsp": {"name": 'Goblin Sapper', "race": "L", "gold": 215, "wood": 100, "food": 2, "level": 4},
    "nhrr": {"name": 'Harpy Rogue', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "nhrw": {"name": 'Harpy Windwitch', "race": "M", "gold": 240, "wood": 30, "food": 2, "level": 3},
    "nits": {"name": 'Ice Troll Berserker', "race": "M", "gold": 245, "wood": 30, "food": 3, "level": 4},
    "nitt": {"name": 'Ice Troll Trapper', "race": "M", "gold": 200, "wood": 20, "food": 2, "level": 3},
    "nkob": {"name": 'Kobold', "race": "M", "gold": 90, "wood": 0, "food": 1, "level": 1},
    "nkog": {"name": 'Kobold Geomancer', "race": "M", "gold": 255, "wood": 30, "food": 2, "level": 3},
    "nthl": {"name": 'Thunder Lizard', "race": "M", "gold": 365, "wood": 150, "food": 6, "level": 6},
    "nmfs": {"name": 'Murloc Flesheater', "race": "M", "gold": 140, "wood": 0, "food": 2, "level": 0},
    "nmrr": {"name": 'Murloc Huntsman', "race": "M", "gold": 150, "wood": 10, "food": 2, "level": 2},
    "nowb": {"name": 'Wildkin', "race": "M", "gold": 195, "wood": 0, "food": 3, "level": 4},
    "nrzm": {"name": 'Razormane Medicine Man', "race": "M", "gold": 350, "wood": 60, "food": 4, "level": 5},
    "nnwa": {"name": 'Nerubian Warrior', "race": "M", "gold": 215, "wood": 0, "food": 2, "level": 3},
    "nnwl": {"name": 'Nerubian Webspinner', "race": "M", "gold": 200, "wood": 35, "food": 3, "level": 3},
    "nogr": {"name": 'Ogre Warrior', "race": "M", "gold": 150, "wood": 0, "food": 2, "level": 3},
    "nogm": {"name": 'Ogre Mauler', "race": "M", "gold": 300, "wood": 0, "food": 4, "level": 5},
    "nogl": {"name": 'Ogre Lord', "race": "M", "gold": 425, "wood": 100, "food": 6, "level": 7},
    "nomg": {"name": 'Ogre Magi', "race": "M", "gold": 320, "wood": 50, "food": 4, "level": 5},
    "nrvs": {"name": 'Frost Revenant', "race": "M", "gold": 255, "wood": 30, "food": 3, "level": 4},
    "nslf": {"name": 'Sludge Flinger', "race": "M", "gold": 255, "wood": 30, "food": 2, "level": 3},
    "nsts": {"name": 'Satyr Shadowdancer', "race": "M", "gold": 255, "wood": 30, "food": 2, "level": 3},
    "nstl": {"name": 'Satyr Soulstealer', "race": "M", "gold": 320, "wood": 50, "food": 4, "level": 5},
    "nzep": {"name": 'Goblin Zeppelin', "race": "L", "gold": 240, "wood": 60, "food": 0, "level": 1},
    "ntrt": {"name": 'Giant Sea Turtle', "race": "M", "gold": 295, "wood": 35, "food": 3, "level": 4},
    "nlds": {"name": 'Makrura Deepseer', "race": "M", "gold": 500, "wood": 100, "food": 4, "level": 5},
    "nlsn": {"name": 'Makrura Snapper', "race": "M", "gold": 315, "wood": 0, "food": 4, "level": 5},
    "nmsn": {"name": "Mur'gul Snarecaster", "race": "M", "gold": 215, "wood": 20, "food": 3, "level": 4},
    "nscb": {"name": 'Spider Crab Shorecrawler', "race": "M", "gold": 105, "wood": 0, "food": 1, "level": 1},
    "nbot": {"name": 'Transport Ship', "race": "M", "gold": 170, "wood": 50, "food": 0, "level": 2},
    "nsc2": {"name": 'Spider Crab Limbripper', "race": "M", "gold": 150, "wood": 0, "food": 2, "level": 3},
    "nsc3": {"name": 'Spider Crab Behemoth', "race": "M", "gold": 300, "wood": 0, "food": 4, "level": 5},
    "nbdm": {"name": 'Blue Dragonspawn Meddler', "race": "M", "gold": 145, "wood": 0, "food": 2, "level": 3},
    "nmgw": {"name": 'Magnataur Warrior', "race": "M", "gold": 340, "wood": 15, "food": 4, "level": 5},
    "nanb": {"name": 'Barbed Arachnathid', "race": "M", "gold": 95, "wood": 5, "food": 1, "level": 1},
    "nanm": {"name": 'Barbed Arachnathid', "race": "M", "gold": 95, "wood": 5, "food": 1, "level": 1},
    "nfps": {"name": 'Polar Furbolg Shaman', "race": "M", "gold": 275, "wood": 30, "food": 3, "level": 4},
    "npfl": {"name": 'Fel Beast', "race": "M", "gold": 155, "wood": 0, "food": 2, "level": 3},
    "ndrd": {"name": 'Draenei Darkslayer', "race": "M", "gold": 260, "wood": 40, "food": 4, "level": 5},
    "ndrm": {"name": 'Draenei Disciple', "race": "M", "gold": 155, "wood": 15, "food": 2, "level": 2},
    "nvdw": {"name": 'Voidwalker', "race": "M", "gold": 155, "wood": 15, "food": 2, "level": 3},
    "nvdg": {"name": 'Greater Voidwalker', "race": "M", "gold": 300, "wood": 45, "food": 4, "level": 6},
    "nnht": {"name": 'Nether Dragon Hatchling', "race": "M", "gold": 215, "wood": 20, "food": 2, "level": 3},
    "nndk": {"name": 'Nether Drake', "race": "M", "gold": 365, "wood": 80, "food": 5, "level": 6},
    "nndr": {"name": 'Nether Dragon', "race": "M", "gold": 745, "wood": 200, "food": 8, "level": 10}
}

creep_codes = {
    "nahy": {"name": "Ancient Hydra", "level": 10, "hp": 1600, "mana": 600},
    "nsqa": {"name": "Ancient Sasquatch", "level": 9, "hp": 1200, "mana": 600},
    "nwna": {"name": "Ancient Wendigo", "level": 9, "hp": 1200, "mana": 600},
    "nwiz": {"name": "Apprentice Wizard", "level": 1, "hp": 180},
    "nane": {"name": "Arachnathid Earth-Borer", "level": 4, "hp": 400, "mana": 200},
    "nano": {"name": "Overlord Arachnathid", "level": 5, "hp": 750},
    "nanw": {"name": "Warrior Arachnathid", "level": 3, "hp": 375},
    "nass": {"name": "Assassin", "level": 4, "hp": 450},
    "nban": {"name": "Bandit", "level": 1, "hp": 240},
    "nbld": {"name": "Bandit Lord", "level": 7, "hp": 950, "mana": 500},
    "nanb": {"name": "Barbed Arachnathid", "level": 1, "hp": 200},
    "nanm": {"name": "Barbed Arachnathid", "level": 1, "hp": 200},
    "narg": {"name": "Battle Golem", "level": 3, "hp": 500},
    "nelb": {"name": "Berserk Elemental", "level": 8, "hp": 1100, "mana": 500},
    "nowk": {"name": "Berserk Wildkin", "level": 8, "hp": 1100, "mana": 500},
    "nbwm": {"name": "Black Dragon", "level": 10, "hp": 2200},
    "nbdr": {"name": "Black Dragon Whelp", "level": 3, "hp": 340},
    "nbdk": {"name": "Black Drake", "level": 6, "hp": 950},
    "nspb": {"name": "Black Spider", "level": 1, "hp": 240},
    "nfgb": {"name": "Bloodfiend", "level": 4, "hp": 450},
    "nadr": {"name": "Blue Dragon", "level": 10, "hp": 2200},
    "nadw": {"name": "Blue Dragon Whelp", "level": 3, "hp": 340},
    "nbda": {"name": "Blue Dragonspawn Apprentice", "level": 4, "hp": 350, "mana": 250},
    "nbdm": {"name": "Blue Dragonspawn Meddler", "level": 3, "hp": 500},
    "nbdo": {"name": "Blue Dragonspawn Overseer", "level": 8, "hp": 1000, "mana": 400},
    "nbds": {"name": "Blue Dragonspawn Sorceror", "level": 6, "hp": 675, "mana": 400},
    "nbdw": {"name": "Blue Dragonspawn Warrior", "level": 5, "hp": 775},
    "nadk": {"name": "Blue Drake", "level": 6, "hp": 950},
    "nbrg": {"name": "Brigand", "level": 2, "hp": 300},
    "nbzd": {"name": "Bronze Dragon", "level": 10, "hp": 2200},
    "nbzw": {"name": "Bronze Dragon Whelp", "level": 3, "hp": 340},
    "nbzk": {"name": "Bronze Drake", "level": 6, "hp": 950},
    "nsbm": {"name": "Brood Mother", "level": 6, "hp": 750},
    "nskf": {"name": "Burning Archer", "level": 3, "traits": "Undead", "hp": 300, "mana": 300},
    "ncer": {"name": "Centaur Drudge", "level": 2, "hp": 300},
    "ncim": {"name": "Centaur Impaler", "level": 4, "hp": 350, "mana": 200},
    "ncnk": {"name": "Centaur Khan", "level": 8, "hp": 900, "mana": 500},
    "ncen": {"name": "Centaur Outrunner", "level": 4, "hp": 550},
    "ncks": {"name": "Centaur Sorceror", "level": 5, "hp": 600, "mana": 400},
    "ncea": {"name": "Centaurarcher", "level": 2, "hp": 300},
    "nenc": {"name": "Corrupted Treant", "level": 1, "hp": 240},
    "nanc": {"name": "Crystal Arachnathid", "level": 1, "hp": 200},
    "ndmu": {"name": "Dalaran Mutant", "level": 2, "hp": 330},
    "ndrj": {"name": "Dalaran Reject", "level": 1, "hp": 240},
    "ndtb": {"name": "Dark Troll Berserker", "level": 4, "hp": 450},
    "ndth": {"name": "Dark Troll High Priest", "level": 4, "hp": 450, "mana": 300},
    "ndtp": {"name": "Dark Troll Shadow Priest", "level": 2, "hp": 240, "mana": 200},
    "nwzd": {"name": "Dark Wizard", "level": 8, "hp": 1200, "mana": 500},
    "ndtr": {"name": "Dark Troll", "level": 2, "hp": 300},
    "ndtt": {"name": "Dark Troll Trapper", "level": 3, "hp": 340},
    "ndtw": {"name": "Dark Troll Warlord", "level": 6, "hp": 750},
    "nrvd": {"name": "Death Revenant", "level": 9, "traits": "Undead", "hp": 1500, "mana": 600},
    "nhdc": {"name": "Deceiver", "level": 3, "hp": 300, "mana": 300},
    "nlrv": {"name": "Deeplord Revenant", "level": 10, "traits": "Undead", "hp": 2100, "mana": 600},
    "nwwd": {"name": "Dire Frost Wolf", "level": 6, "hp": 750, "mana": 400},
    "nmdr": {"name": "Dire Mammoth", "level": 8, "hp": 1550},
    "nwld": {"name": "Dire Wolf", "level": 6, "hp": 750, "mana": 400},
    "nbal": {"name": "Doom Guard", "level": 8, "hp": 1350, "mana": 500},
    "ndrd": {"name": "Draenei Darkslayer", "level": 5, "hp": 525, "mana": 300},
    "ndrm": {"name": "Draenei Disciple", "level": 2, "hp": 280, "mana": 200},
    "ndrf": {"name": "Draenei Guardian", "level": 1, "hp": 240},
    "ndrh": {"name": "Draenei Harbinger", "level": 4, "hp": 450, "mana": 400},
    "ndrp": {"name": "Draenei Protector", "level": 2, "hp": 325},
    "ndrs": {"name": "Draenei Seer", "level": 6, "hp": 775, "mana": 500},
    "ndrw": {"name": "Draenei Watcher", "level": 3, "hp": 400},
    "nws1": {"name": "Dragon Hawk", "level": 5, "hp": 700},
    "ntrd": {"name": "Dragon Turtle", "level": 10, "hp": 2000, "mana": 600},
    "nehy": {"name": "Elder Hydra", "level": 7, "hp": 850, "mana": 400},
    "njga": {"name": "Elder Jungle Stalker", "level": 6, "hp": 900},
    "nsqe": {"name": "Elder Sasquatch", "level": 6, "hp": 950, "mana": 400},
    "nvde": {"name": "Elder Voidwalker", "level": 9, "hp": 1500, "mana": 500},
    "nwnr": {"name": "Elder Wendigo", "level": 6, "hp": 950},
    "nenf": {"name": "Enforcer", "level": 5, "hp": 500},
    "nele": {"name": "Enraged Elemental", "level": 4, "hp": 550},
    "nowe": {"name": "Enraged Wildkin", "level": 6, "hp": 950},
    "njgb": {"name": "Enranged Jungle Stalker", "level": 9, "hp": 1600, "mana": 600},
    "nerd": {"name": "Eredar Diabolist", "level": 6, "hp": 630, "mana": 300},
    "ners": {"name": "Eredar Sorceror", "level": 4, "hp": 425, "mana": 200},
    "nerw": {"name": "Eredar Warlock", "level": 9, "hp": 1350, "mana": 500},
    "nfod": {"name": "Faceless One Deathbringer", "level": 10, "hp": 1900, "mana": 500},
    "nfot": {"name": "Faceless One Terror", "level": 8, "hp": 1150, "mana": 400},
    "nfor": {"name": "Faceless One Trickster", "level": 6, "hp": 675, "mana": 300},
    "nhfp": {"name": "Fallen Priest", "level": 1, "hp": 240},
    "npfl": {"name": "Fel Beast", "level": 3, "hp": 390},
    "npfm": {"name": "Fel Ravager", "level": 7, "hp": 950, "mana": 300},
    "nfel": {"name": "Fel Stalker", "level": 5, "hp": 750, "mana": 200},
    "nfgu": {"name": "Felguard", "level": 2, "hp": 300},
    "nrvf": {"name": "Fire Revenant", "level": 3, "traits": "Undead", "hp": 340, "mana": 300},
    "nftb": {"name": "Forest Troll Berserker", "level": 4, "hp": 450},
    "nfsh": {"name": "Forest Troll High Priest", "level": 4, "hp": 450, "mana": 300},
    "nfsp": {"name": "Forest Troll Shadow Priest", "level": 2, "hp": 240, "mana": 200},
    "nftk": {"name": "Forest Troll Warlord", "level": 6, "hp": 750},
    "nftr": {"name": "Forest Troll", "level": 2, "hp": 300},
    "nftt": {"name": "Forest Troll Trapper", "level": 3, "hp": 400},
    "nfgo": {"name": "Forgotten One", "level": 15, "hp": 4000, "mana": 1000},
    "nfgt": {"name": "Forgotten One Tentacle", "level": 1, "traits": "Ward", "hp": 200},
    "nrvs": {"name": "Frost Revenant", "level": 4, "traits": "Undead", "hp": 450, "mana": 300},
    "nfrl": {"name": "Furbolg", "level": 4, "hp": 550},
    "nfrg": {"name": "Furbolg Champion", "level": 7, "hp": 950},
    "nfre": {"name": "Furbolg Elder Shaman", "level": 7, "hp": 950, "mana": 500},
    "nfrp": {"name": "Pandaren", "level": 4, "hp": 550},
    "nfrs": {"name": "Furbolg Shaman", "level": 4, "hp": 550, "mana": 300},
    "nfrb": {"name": "Furbolg Tracker", "level": 6, "hp": 950, "mana": 400},
    "nfra": {"name": "Furbolg Ursa Warrior", "level": 8, "hp": 1100, "mana": 500},
    "ntrg": {"name": "Gargantuan Sea Turtle", "level": 7, "hp": 1250},
    "ngh1": {"name": "Ghost", "level": 3, "traits": "Undead", "hp": 300, "mana": 300},
    "nplg": {"name": "Giant Polar Bear", "level": 6, "hp": 900},
    "ntrt": {"name": "Giant Sea Turtle", "level": 4, "hp": 375},
    "nskg": {"name": "Giant Skeleton Warrior", "level": 3, "traits": "Undead", "hp": 380},
    "nsgt": {"name": "Giant Spider", "level": 4, "hp": 550},
    "nwwg": {"name": "Giant Frost Wolf", "level": 4, "hp": 550},
    "nwlg": {"name": "Giant Wolf", "level": 4, "hp": 550},
    "ngns": {"name": "Gnoll Assassin", "level": 3, "hp": 320},
    "ngnb": {"name": "Gnoll Brute", "level": 3, "hp": 400},
    "ngnv": {"name": "Gnoll Overseer", "level": 5, "hp": 750},
    "ngna": {"name": "Gnoll Poacher", "level": 1, "hp": 240},
    "ngno": {"name": "Gnoll", "level": 1, "hp": 240},
    "ngnw": {"name": "Gnoll Warden", "level": 3, "hp": 330, "mana": 300},
    "nggr": {"name": "Granite Golem", "level": 9, "hp": 1500, "mana": 600},
    "nvdg": {"name": "Greater Voidwalker", "level": 6, "hp": 750, "mana": 400},
    "ngrd": {"name": "Green Dragon", "level": 10, "hp": 2200},
    "ngrw": {"name": "Green Dragon Whelp", "level": 3, "hp": 340},
    "ngdk": {"name": "Green Drake", "level": 6, "hp": 950},
    "nspg": {"name": "Forest Spider", "level": 1, "hp": 240},
    "nhrh": {"name": "Harpy Storm-hag", "level": 5, "hp": 600, "mana": 400},
    "nhrq": {"name": "Harpy Queen", "level": 7, "hp": 750, "mana": 400},
    "nhrr": {"name": "Harpy Rogue", "level": 3, "hp": 340},
    "nhar": {"name": "Harpy Scout", "level": 1, "hp": 210},
    "nhrw": {"name": "Harpy Windwitch", "level": 3, "hp": 280, "mana": 300},
    "nwe1": {"name": "Hawk", "level": 2, "hp": 300},
    "nhhr": {"name": "Heretic", "level": 5, "hp": 600, "mana": 400},
    "nhyd": {"name": "Hydra", "level": 6, "hp": 575},
    "nhyh": {"name": "Hydra Hatchling", "level": 3, "hp": 350},
    "nhym": {"name": "Hydromancer", "level": 2, "hp": 405, "mana": 400},
    "nrvi": {"name": "Ice Revenant", "level": 8, "traits": "Undead", "hp": 1100, "mana": 500},
    "nits": {"name": "Ice Troll Berserker", "level": 4, "hp": 450},
    "nith": {"name": "Ice Troll High Priest", "level": 4, "hp": 450, "mana": 300},
    "nitp": {"name": "Ice Troll Priest", "level": 2, "hp": 240, "mana": 200},
    "nitt": {"name": "Ice Troll Trapper", "level": 3, "hp": 400},
    "nitw": {"name": "Ice Troll Warlord", "level": 6, "hp": 750},
    "nitr": {"name": "Ice Troll", "level": 2, "hp": 300},
    "nmit": {"name": "Icetusk Mammoth", "level": 5, "hp": 925},
    "ninf": {"name": "Infernal", "level": 8, "hp": 1500, "mana": "-"},
    "nina": {"name": "Infernal Automaton", "level": 10, "traits": "Mechanical", "hp": 1500, "mana": 400},
    "ninc": {"name": "Infernal Contraption", "level": 5, "traits": "Mechanical", "hp": 600},
    "ninm": {"name": "Infernal Machine", "level": 8, "traits": "Mechanical", "hp": 1200, "mana": 350},
    "njg1": {"name": "Jungle Stalker", "level": 3, "hp": 400},
    "nkob": {"name": "Kobold", "level": 1, "hp": 240},
    "nkog": {"name": "Kobold Geomancer", "level": 3, "hp": 300, "mana": 300},
    "nkol": {"name": "Kobold Taskmaster", "level": 5, "hp": 650},
    "nkot": {"name": "Kobold Tunneler", "level": 3, "hp": 325},
    "nvdl": {"name": "Lesser Voidwalker", "level": 1, "hp": 240},
    "nltl": {"name": "Lightning Lizard", "level": 2, "hp": 280, "mana": 200},
    "nrvl": {"name": "Lightning Revenant", "level": 6, "traits": "Undead", "hp": 750, "mana": 400},
    "nmgd": {"name": "Magnataur Destroyer", "level": 10, "hp": 2100, "mana": 500},
    "nmgr": {"name": "Magnataur Reaver", "level": 8, "hp": 1500, "mana": 350},
    "nmgw": {"name": "Magnataur Warrior", "level": 5, "hp": 900},
    "ndqp": {"name": "Maiden of Pain", "level": 8, "hp": 1050, "mana": 400},
    "nlds": {"name": "Makrura Deepseer", "level": 5, "hp": 480, "mana": 300},
    "nlpd": {"name": "Makrura Pooldweller", "level": 2, "hp": 210},
    "nlpr": {"name": "Makrura Prawn", "level": 1, "hp": 170},
    "nlps": {"name": "Makrura Prawn", "level": 1, "hp": 170},
    "nlsn": {"name": "Makrura Snapper", "level": 5, "hp": 620},
    "nlkl": {"name": "Makrura Tidal Lord", "level": 7, "hp": 800},
    "nltc": {"name": "Makrura Tidecaller", "level": 2, "hp": 240, "mana": 300},
    "nmam": {"name": "Mammoth", "level": 3, "hp": 450},
    "ngrk": {"name": "Mud Golem", "level": 2, "hp": 240, "mana": 300},
    "nmbg": {"name": "Mur'gul Blood-Gill", "level": 2, "hp": 300, "mana": 200},
    "nmcf": {"name": "Mur'gul Cliffrunner", "level": 1, "hp": 240},
    "nmrv": {"name": "Mur'gul Maurader", "level": 6, "hp": 1000},
    "nmsc": {"name": "Mur'gul Shadowcaster", "level": 7, "hp": 1000, "mana": 400},
    "nmsn": {"name": "Mur'gul Snarecaster", "level": 4, "hp": 375, "mana": 300},
    "nmtw": {"name": "Mur'gul Tidewarrior", "level": 3, "hp": 400},
    "nmfs": {"name": "Murloc Flesheater", "level": 3, "hp": 400},
    "nmrr": {"name": "Murloc Huntsman", "level": 2, "hp": 300},
    "nmmu": {"name": "Murloc Mutant", "level": 6, "hp": 750, "mana": 400},
    "nmrm": {"name": "Murloc Nightcrawler", "level": 3, "hp": 400},
    "nmpg": {"name": "Murloc Plaguebearer", "level": 2, "hp": 180},
    "nmrl": {"name": "Murloc Tiderunner", "level": 1, "hp": 240},
    "nnwq": {"name": "Nerubian Queen", "level": 7, "hp": 950, "mana": 500},
    "nnwr": {"name": "Nerubian Seer", "level": 5, "hp": 600, "mana": 400},
    "nnws": {"name": "Nerubian Spider Lord", "level": 5, "hp": 750},
    "nnwa": {"name": "Nerubian Warrior", "level": 3, "hp": 400},
    "nnwl": {"name": "Nerubian Webspinner", "level": 3, "hp": 350, "mana": 300},
    "nndr": {"name": "Nether Dragon", "level": 10, "hp": 2200, "mana": 500},
    "nnht": {"name": "Nether Dragon Hatchling", "level": 3, "hp": 340},
    "nndk": {"name": "Nether Drake", "level": 6, "hp": 950},
    "nogl": {"name": "Ogre Lord", "level": 7, "hp": 950, "mana": 500},
    "nomg": {"name": "Ogre Magi", "level": 5, "hp": 600, "mana": 400},
    "nogm": {"name": "Ogre Mauler", "level": 5, "hp": 850},
    "nogr": {"name": "Ogre Warrior", "level": 3, "hp": 400},
    "nfov": {"name": "Overlord", "level": 6, "hp": 775, "mana": 300},
    "nepl": {"name": "Plague Treant", "level": 5, "hp": 600, "mana": 400},
    "nenp": {"name": "Poison Treant", "level": 3, "hp": 290, "mana": 300},
    "nplb": {"name": "Polar Bear", "level": 4, "hp": 475},
    "nfpl": {"name": "Polar Furbolg", "level": 4, "hp": 550},
    "nfpc": {"name": "Polar Furbolg Champion", "level": 7, "hp": 950},
    "nfpe": {"name": "Polar Furbolg Elder Shaman", "level": 8, "hp": 950, "mana": 500},
    "nfps": {"name": "Polar Furbolg Shaman", "level": 4, "hp": 550, "mana": 300},
    "nfpt": {"name": "Polar Furbolg Tracker", "level": 6, "hp": 950, "mana": 400},
    "nfpu": {"name": "Polar Furbolg Ursa Warrior", "level": 8, "hp": 1100, "mana": 500},
    "ndqs": {"name": "Queen Of Suffering", "level": 10, "hp": 1600, "mana": 500},
    "nrzt": {"name": "Quillboar", "level": 1, "hp": 240},
    "nqbh": {"name": "Quillboar Hunter", "level": 3, "hp": 375},
    "nrzb": {"name": "Razormane Brute", "level": 3, "hp": 400},
    "nrzg": {"name": "Razormane Chieftain", "level": 7, "hp": 950, "mana": 500},
    "nrzm": {"name": "Razormane Medicine Man", "level": 5, "hp": 600, "mana": 400},
    "nrzs": {"name": "Razormane Scout", "level": 1, "hp": 240},
    "nrwm": {"name": "Red Dragon", "level": 10, "hp": 2200},
    "nrdk": {"name": "Red Dragon Whelp", "level": 3, "hp": 400},
    "nrdr": {"name": "Red Drake", "level": 6, "hp": 950},
    "nrel": {"name": "Reef Elemental", "level": 2, "hp": 300},
    "nwzg": {"name": "Renegade Wizard", "level": 5, "hp": 600, "mana": 400},
    "ndrv": {"name": "Revenant of the Depths", "level": 8, "traits": "Undead", "hp": 1000, "mana": 500},
    "nsrv": {"name": "Revenant of the Seas", "level": 5, "traits": "Undead", "hp": 900},
    "ntrv": {"name": "Revenant of the Tides", "level": 3, "traits": "Undead", "hp": 375},
    "ngst": {"name": "Rock Golem", "level": 6, "hp": 675, "mana": 400},
    "nrog": {"name": "Rogue", "level": 3, "hp": 400},
    "nwzr": {"name": "Rogue Wizard", "level": 3, "hp": 340, "mana": 300},
    "nslr": {"name": "Salamander", "level": 5, "hp": 600, "mana": 400},
    "nslh": {"name": "Salamander Hatchling", "level": 3, "hp": 400},
    "nsll": {"name": "Salamander Lord", "level": 10, "hp": 1800, "mana": 700},
    "nslv": {"name": "Salamander Vizier", "level": 7, "hp": 950, "mana": 500},
    "nsqt": {"name": "Sasquatch", "level": 5, "hp": 750},
    "nsqo": {"name": "Sasquatch Oracle", "level": 7, "hp": 950, "mana": 500},
    "nsty": {"name": "Satyr", "level": 1, "hp": 240},
    "nsth": {"name": "Satyr Hellcaller", "level": 9, "hp": 1100, "mana": 500},
    "nsts": {"name": "Satyr Shadowdancer", "level": 3, "hp": 340, "mana": 300},
    "nstl": {"name": "Satyr Soulstealer", "level": 5, "hp": 600, "mana": 400},
    "nsat": {"name": "Satyr Trickster", "level": 1, "hp": 240, "mana": 200},
    "nsel": {"name": "Sea Elemental", "level": 5, "hp": 550},
    "nsgn": {"name": "Sea Giant", "level": 3, "hp": 350},
    "nsgb": {"name": "Sea Giant Behemoth", "level": 8, "hp": 1000, "mana": 400},
    "nsgh": {"name": "Sea Giant Hunter", "level": 5, "hp": 725},
    "ntrs": {"name": "Sea Turtle", "level": 2, "hp": 250},
    "ntrh": {"name": "Sea Turtle Hatchling", "level": 1, "hp": 220},
    "nsgg": {"name": "Siege Golem", "level": 9, "hp": 1900},
    "nska": {"name": "Skeleton Archer", "level": 1, "traits": "Undead", "hp": 180},
    "nskm": {"name": "Skeletal Marksman", "level": 3, "traits": "Undead", "hp": 300, "mana": 300},
    "nsko": {"name": "Skeletal Orc", "level": 3, "traits": "Undead", "hp": 375},
    "nsoc": {"name": "Skeletal Orc Champion", "level": 8, "traits": "Undead", "hp": 1100, "mana": 400},
    "nsog": {"name": "Skeletal Orc Grunt", "level": 5, "traits": "Undead", "hp": 850},
    "nske": {"name": "Skeletonwarrior", "level": 1, "traits": "Undead", "hp": 180},
    "nslf": {"name": "Sludge Flinger", "level": 3, "hp": 340, "mana": 300},
    "nslm": {"name": "Sludge Minion", "level": 1, "hp": 240, "mana": 200},
    "nsln": {"name": "Sludge Monstrosity", "level": 5, "hp": 600, "mana": 400},
    "nspr": {"name": "Spider", "level": 1, "hp": 240},
    "nscb": {"name": "Spider Crab Shorecrawler", "level": 1, "hp": 240},
    "nsc2": {"name": "Spider Crab Limbripper", "level": 3, "hp": 400},
    "nsc3": {"name": "Spider Crab Behemoth", "level": 5, "hp": 850},
    "nspd": {"name": "Spiderling", "level": 1, "hp": 240},
    "nspp": {"name": "Spirit Pig", "level": 2, "hp": 200},
    "nssp": {"name": "Spitting Spider", "level": 3, "hp": 400},
    "nogn": {"name": "Stonemaul Magi", "level": 7, "hp": 1060, "mana": 400},
    "nogo": {"name": "Stonemaul Ogre", "level": 6, "hp": 1060},
    "noga": {"name": "Stonemaul Warchief", "level": 11, "hp": 3300},
    "nstw": {"name": "Storm Wyrm", "level": 9, "hp": 1500, "mana": 600},
    "nsra": {"name": "Stormreaver Apprentice", "level": 1, "hp": 240},
    "nsrh": {"name": "Stormreaver Hermit", "level": 3, "hp": 340, "mana": 200},
    "nsrn": {"name": "Stormreaver Necrolyte", "level": 6, "hp": 675, "mana": 350},
    "nsrw": {"name": "Stormreaver Warlock", "level": 9, "hp": 1500, "mana": 500},
    "ndqn": {"name": "Succubus", "level": 3, "hp": 400},
    "nthl": {"name": "Thunder Lizard", "level": 6, "hp": 750, "mana": 400},
    "nwlt": {"name": "Timber Wolf", "level": 2, "hp": 300},
    "ntkc": {"name": "Tuskarr Chieftain", "level": 7, "hp": 950, "mana": "-"},
    "ntkf": {"name": "Tuskarr Fighter", "level": 2, "hp": 250},
    "ntkh": {"name": "Tuskarr Healer", "level": 3, "hp": 300, "mana": 200},
    "ntks": {"name": "Tuskarr Sorceror", "level": 5, "hp": 475, "mana": 300},
    "ntka": {"name": "Tuskarr Spearman", "level": 2, "hp": 300},
    "ntkt": {"name": "Tuskarr Trapper", "level": 4, "hp": 475},
    "ntkw": {"name": "Tuskarr Warrior", "level": 4, "hp": 475},
    "nubk": {"name": "Unbroken Darkhunter", "level": 2, "hp": 250},
    "nubw": {"name": "Unbroken Darkweaver", "level": 5, "hp": 600, "mana": 200},
    "nubr": {"name": "Unbroken Rager", "level": 4, "hp": 475},
    "ndqt": {"name": "Vile Temptress", "level": 6, "hp": 750},
    "ndqv": {"name": "Vile Tormentor", "level": 5, "hp": 510, "mana": 200},
    "nvdw": {"name": "Voidwalker", "level": 3, "hp": 365, "mana": 200},
    "nwrg": {"name": "War Golem", "level": 6, "hp": 1000},
    "ncfs": {"name": "Watery Minion Cliffrunner", "level": 2, "hp": 240},
    "nsns": {"name": "Watery Minion Snarecaster", "level": 3, "hp": 375, "mana": 300},
    "ntws": {"name": "Watery Minion Tidewarrior", "level": 2, "hp": 400},
    "nwen": {"name": "Wendigo", "level": 4, "hp": 550},
    "nwns": {"name": "Wendigo Shaman", "level": 7, "hp": 950, "mana": 500},
    "nwwf": {"name": "Frost Wolf", "level": 2, "hp": 300},
    "nowb": {"name": "Wildkin", "level": 4, "hp": 550},
    "ngh2": {"name": "Wraith", "level": 6, "traits": "Undead", "hp": 750, "mana": 400},
    "nzom": {"name": "Zombie", "level": 1, "traits": "Undead", "hp": 240}
}

building_codes = {
    "hhou": {'name': 'Farm', 'race': 'H', 'gold': 80, 'wood': 20, 'tier': 1, 'upgrade': False, 'tower': False},
    "halt": {'name': 'Altar of Kings', 'race': 'H', 'gold': 180, 'wood': 50, 'tier': 1, 'upgrade': False, 'tower': False},
    "harm": {'name': 'Workshop', 'race': 'H', 'gold': 140, 'wood': 140, 'tier': 2, 'upgrade': False, 'tower': False},
    "hars": {'name': 'Arcane Sanctum', 'race': 'H', 'gold': 150, 'wood': 140, 'tier': 2, 'upgrade': False, 'tower': False},
    "hbar": {'name': 'Barracks', 'race': 'H', 'gold': 160, 'wood': 60, 'tier': 1, 'upgrade': False, 'tower': False},
    "hbla": {'name': 'Blacksmith', 'race': 'H', 'gold': 140, 'wood': 60, 'tier': 1, 'upgrade': False, 'tower': False},
    "hgra": {'name': 'Gryphon Aviary', 'race': 'H', 'gold': 140, 'wood': 150, 'tier': 2, 'upgrade': False, 'tower': False},
    "hwtw": {'name': 'Scout Tower', 'race': 'H', 'gold': 30, 'wood': 20, 'tier': 1, 'upgrade': False, 'tower': False},
    "hvlt": {'name': 'Arcane Vault', 'race': 'H', 'gold': 130, 'wood': 30, 'tier': 1, 'upgrade': False, 'tower': False},
    "hlum": {'name': 'Lumber Mill', 'race': 'H', 'gold': 120, 'wood': 0, 'tier': 1, 'upgrade': False, 'tower': False},
    "htow": {'name': 'Town Hall', 'race': 'H', 'gold': 385, 'wood': 205, 'tier': 1, 'upgrade': False, 'tower': False},
    "hkee": {'name': 'Keep', 'race': 'H', 'gold': 320, 'wood': 210, 'tier': 1, 'upgrade': True, 'tower': False},
    "hcas": {'name': 'Castle', 'race': 'H', 'gold': 360, 'wood': 210, 'tier': 2, 'upgrade': True, 'tower': False},
    "hctw": {'name': 'Cannon Tower', 'race': 'H', 'gold': 120, 'wood': 100, 'tier': 2, 'upgrade': True, 'tower': True},
    "hgtw": {'name': 'Guard Tower', 'race': 'H', 'gold': 70, 'wood': 50, 'tier': 1, 'upgrade': True, 'tower': True},
    "hatw": {'name': 'Arcane Tower', 'race': 'H', 'gold': 70, 'wood': 50, 'tier': 1, 'upgrade': True, 'tower': True},

    "etrp": {'name': 'Ancient Protector', 'race': 'N', 'gold': 135, 'wood': 80, 'tier': 1, 'upgrade': False, 'tower': True},
    "etol": {'name': 'Tree of Life', 'race':  'N', 'gold': 340, 'wood': 185, 'tier': 1, 'upgrade': False, 'tower': False},
    "edob": {'name': "Hunter's Hall", 'race':  'N', 'gold': 210, 'wood': 100, 'tier': 1, 'upgrade': False, 'tower': False},
    "eate": {'name': 'Altar of Elders', 'race':  'N', 'gold': 180, 'wood': 50, 'tier': 1, 'upgrade': False, 'tower': False},
    "eden": {'name': 'Ancient of Wonders', 'race':  'N', 'gold': 90, 'wood': 30, 'tier': 1, 'upgrade': False, 'tower': False},
    "eaoe": {'name': 'Ancient of Lore', 'race':  'N', 'gold': 155, 'wood': 145, 'tier': 2, 'upgrade': False, 'tower': False},
    "eaom": {'name': 'Ancient of War', 'race':  'N', 'gold': 150, 'wood': 60, 'tier': 1, 'upgrade': False, 'tower': False},
    "eaow": {'name': 'Ancient of Wind', 'race':  'N', 'gold': 150, 'wood': 140, 'tier': 2, 'upgrade': False, 'tower': False},
    "edos": {'name': 'Chimaera Roost', 'race':  'N', 'gold': 140, 'wood': 190, 'tier': 3, 'upgrade': False, 'tower': False},
    "emow": {'name': 'Moon Well', 'race':  'N', 'gold': 180, 'wood': 40, 'tier': 1, 'upgrade': False, 'tower': False},
    "etoa": {'name': 'Tree of Ages', 'race':  'N', 'gold': 320, 'wood': 180, 'tier': 1, 'upgrade': True, 'tower': False},
    "etoe": {'name': 'Tree of Eternity', 'race':  'N', 'gold': 330, 'wood': 200, 'tier': 2, 'upgrade': True, 'tower': False},

    "oalt": {'name': 'Altar of Storms', 'race': 'O', 'gold': 180, 'wood': 50, 'tier': 1, 'upgrade': False, 'tower': False},
    "obar": {'name': 'Barracks', 'race': 'O', 'gold': 180, 'wood': 50, 'tier': 1, 'upgrade': False, 'tower': False},
    "obea": {'name': 'Beastiary', 'race': 'O', 'gold': 145, 'wood': 140, 'tier': 2, 'upgrade': False, 'tower': False},
    "ofor": {'name': 'War Mill', 'race': 'O', 'gold': 205, 'wood': 0, 'tier': 1, 'upgrade': False, 'tower': False},
    "ogre": {'name': 'Great Hall', 'race': 'O', 'gold': 385, 'wood': 185, 'tier': 1, 'upgrade': False, 'tower': False},
    "osld": {'name': 'Spirit Lodge', 'race': 'O', 'gold': 150, 'wood': 150, 'tier': 2, 'upgrade': False, 'tower': False},
    "otrb": {'name': 'Orc Burrow', 'race': 'O', 'gold': 160, 'wood': 40, 'tier': 1, 'upgrade': False, 'tower': False},
    "orbr": {'name': 'Reinforced Orc Burrow', 'race': 'O', 'gold': 160, 'wood': 40, 'tier': 2, 'upgrade': False, 'tower': False},
    "otto": {'name': 'Tauren Totem', 'race': 'O', 'gold': 135, 'wood': 155, 'tier': 2, 'upgrade': False, 'tower': False},
    "ovln": {'name': 'Voodoo Lounge', 'race': 'O', 'gold': 130, 'wood': 30, 'tier': 1, 'upgrade': False, 'tower': False},
    "owtw": {'name': 'Watch Tower', 'race': 'O', 'gold': 110, 'wood': 80, 'tier': 1, 'upgrade': False, 'tower': True},
    "ostr": {'name': 'Stronghold', 'race': 'O', 'gold': 315, 'wood': 190, 'tier': 1, 'upgrade': True, 'tower': False},
    "ofrt": {'name': 'Fortress', 'race': 'O', 'gold': 325, 'wood': 190, 'tier': 2, 'upgrade': True, 'tower': False},

    "uaod": {'name': 'Altar of Darkness', 'race': 'U', 'gold': 180, 'wood': 50, 'tier': 1, 'upgrade': False, 'tower': False},
    "unpl": {'name': 'Necropolis', 'race': 'U', 'gold': 225, 'wood': 0, 'tier': 1, 'upgrade': False, 'tower': False},
    "usep": {'name': 'Crypt', 'race': 'U', 'gold': 200, 'wood': 50, 'tier': 1, 'upgrade': False, 'tower': False},
    "utod": {'name': 'Temple of the Damned', 'race': 'U', 'gold': 155, 'wood': 140, 'tier': 2, 'upgrade': False, 'tower': False},
    "utom": {'name': 'Tomb of Relics', 'race': 'U', 'gold': 130, 'wood': 30, 'tier': 1, 'upgrade': False, 'tower': False},
    "ugol": {'name': 'Haunted Gold Mine', 'race': 'U', 'gold': 225, 'wood': 210, 'tier': 1, 'upgrade': False, 'tower': False},
    "uzig": {'name': 'Ziggurat', 'race': 'U', 'gold': 150, 'wood': 50, 'tier': 1, 'upgrade': False, 'tower': False},
    "ubon": {'name': 'Boneyard', 'race': 'U', 'gold': 175, 'wood': 200, 'tier': 3, 'upgrade': False, 'tower': False},
    "usap": {'name': 'Sacrificial Pit', 'race': 'U', 'gold': 75, 'wood': 150, 'tier': 2, 'upgrade': False, 'tower': False},
    "uslh": {'name': 'Slaughterhouse', 'race': 'U', 'gold': 140, 'wood': 135, 'tier': 2, 'upgrade': False, 'tower': False},
    "ugrv": {'name': 'Graveyard', 'race': 'U', 'gold': 215, 'wood': 0, 'tier': 1, 'upgrade': False, 'tower': False},
    "unp1": {'name': 'Halls of the Dead', 'race': 'U', 'gold': 320, 'wood': 210, 'tier': 1, 'upgrade': False, 'tower': False},
    "unp2": {'name': 'Black Citadel', 'race': 'U', 'gold': 325, 'wood': 230, 'tier': 2, 'upgrade': False, 'tower': False},
    "uzg1": {'name': 'Spirit Tower', 'race': 'U', 'gold': 145, 'wood': 40, 'tier': 1, 'upgrade': True, 'tower': True},
    "uzg2": {'name': 'Nerubian Tower', 'race': 'U', 'gold': 100, 'wood': 20, 'tier': 1, 'upgrade': True, 'tower': True}
}

color_names = {
    '#ff0303': 'red',
    '#0042ff': 'blue',
    '#1ce6b9': 'teal',
    '#540081': 'purple',
    '#fffc00': 'yellow',
    '#fe8a0e': 'orange',
    '#20c000': 'green',
    '#e55bb0': 'pink',
    '#959697': 'gray',
    '#7ebff1': 'light blue',
    '#106246': 'dark green',
    '#4a2a04': 'brown',
    '#9b0000': 'maroon',
    '#0000c3': 'navy',
    '#00eaff': 'turquoise',
    '#be00fe': 'violet',
    '#ebcd87': 'wheat',
    '#f8a48b': 'peach',
    '#bfff80': 'mint',
    '#dcb9eb': 'lavender',
    '#282828': 'coal',
    '#ebf0ff': 'snow',
    '#00781e': 'emerald',
    '#a46f33': 'peanut'
}

ability_codes = {
    'AHbz': {'hero': 'Hamg', 'name': 'Blizzard', 'ult': False},
    'AHwe': {'hero': 'Hamg', 'name': 'Summon Water Elemental', 'ult': False},
    'AHab': {'hero': 'Hamg', 'name': 'Brilliance Aura', 'ult': False},
    'AHmt': {'hero': 'Hamg', 'name': 'Mass Teleport', 'ult': True},
    'AHtb': {'hero': 'Hmkg', 'name': 'Storm Bolt', 'ult': False},
    'AHtc': {'hero': 'Hmkg', 'name': 'Thunder Clap', 'ult': False},
    'AHbh': {'hero': 'Hmkg', 'name': 'Bash', 'ult': False},
    'AHav': {'hero': 'Hmkg', 'name': 'Avatar', 'ult': True},
    'AHhb': {'hero': 'Hpal', 'name': 'Holy Light', 'ult': False},
    'AHds': {'hero': 'Hpal', 'name': 'Divine Shield', 'ult': False},
    'AHad': {'hero': 'Hpal', 'name': 'Devotion Aura', 'ult': False},
    'AHre': {'hero': 'Hpal', 'name': 'Resurrection', 'ult': True},
    'AHdr': {'hero': 'Hblm', 'name': 'Siphon Mana', 'ult': False},
    'AHfs': {'hero': 'Hblm', 'name': 'Flame Strike', 'ult': False},
    'AHbn': {'hero': 'Hblm', 'name': 'Banish', 'ult': False},
    'AHpx': {'hero': 'Hblm', 'name': 'Summon Phoenix', 'ult': True},

    'AEmb': {'hero': 'Edem', 'name': 'Mana Burn', 'ult': False},
    'AEim': {'hero': 'Edem', 'name': 'Immolation', 'ult': False},
    'AEev': {'hero': 'Edem', 'name': 'Evasion', 'ult': False},
    'AEme': {'hero': 'Edem', 'name': 'Metamorphosis', 'ult': True},
    'AEer': {'hero': 'Ekee', 'name': 'Entangling Roots', 'ult': False},
    'AEfn': {'hero': 'Ekee', 'name': 'Force of Nature', 'ult': False},
    'AEah': {'hero': 'Ekee', 'name': 'Thorns Aura', 'ult': False},
    'AEtq': {'hero': 'Ekee', 'name': 'Tranquility', 'ult': True},
    'AEst': {'hero': 'Emoo', 'name': 'Scout', 'ult': False},
    'AHfa': {'hero': 'Emoo', 'name': 'Searing Arrows', 'ult': False},
    'AEar': {'hero': 'Emoo', 'name': 'Trueshot Aura', 'ult': False},
    'AEsf': {'hero': 'Emoo', 'name': 'Starfall', 'ult': True},
    'AEbl': {'hero': 'Ewar', 'name': 'Blink', 'ult': False},
    'AEfk': {'hero': 'Ewar', 'name': 'Fan of Knives', 'ult': False},
    'AEsh': {'hero': 'Ewar', 'name': 'Shadow Strike', 'ult': False},
    'AEsv': {'hero': 'Ewar', 'name': 'Spirit of Vengeance', 'ult': True},

    'AOwk': {'hero': 'Obla', 'name': 'Wind Walk', 'ult': False},
    'AOmi': {'hero': 'Obla', 'name': 'Mirror Image', 'ult': False},
    'AOcr': {'hero': 'Obla', 'name': 'Critical Strike', 'ult': False},
    'AOww': {'hero': 'Obla', 'name': 'Bladestorm', 'ult': True},
    'AOcl': {'hero': 'Ofar', 'name': 'Chain Lighting', 'ult': False},
    'AOfs': {'hero': 'Ofar', 'name': 'Far Sight', 'ult': False},
    'AOsf': {'hero': 'Ofar', 'name': 'Feral Spirit', 'ult': False},
    'AOeq': {'hero': 'Ofar', 'name': 'Earth Quake', 'ult': True},
    'AOsh': {'hero': 'Otch', 'name': 'Shockwave', 'ult': False},
    'AOae': {'hero': 'Otch', 'name': 'Endurance Aura', 'ult': False},
    'AOws': {'hero': 'Otch', 'name': 'War Stomp', 'ult': False},
    'AOre': {'hero': 'Otch', 'name': 'Reincarnation', 'ult': True},
    'AOhw': {'hero': 'Oshd', 'name': 'Healing Wave', 'ult': False},
    'AOhx': {'hero': 'Oshd', 'name': 'Hex', 'ult': False},
    'AOsw': {'hero': 'Oshd', 'name': 'Serpent Ward', 'ult': False},
    'AOvd': {'hero': 'Oshd', 'name': 'Big Bad Voodoo', 'ult': True},

    'AUdc': {'hero': 'Udea', 'name': 'Death Coil', 'ult': False},
    'AUdp': {'hero': 'Udea', 'name': 'Death Pact', 'ult': False},
    'AUau': {'hero': 'Udea', 'name': 'Unholy Aura', 'ult': False},
    'AUan': {'hero': 'Udea', 'name': 'Animate Dead', 'ult': True},
    'AUcs': {'hero': 'Udre', 'name': 'Carrion Swarm', 'ult': False},
    'AUsl': {'hero': 'Udre', 'name': 'Sleep', 'ult': False},
    'AUav': {'hero': 'Udre', 'name': 'Vampiric Aura', 'ult': False},
    'AUin': {'hero': 'Udre', 'name': 'Inferno', 'ult': True},
    'AUfn': {'hero': 'Ulic', 'name': 'Frost Nova', 'ult': False},
    'AUfa': {'hero': 'Ulic', 'name': 'Frost Armor', 'ult': False},
    'AUfu': {'hero': 'Ulic', 'name': 'Frost Armor', 'ult': False},
    'AUdr': {'hero': 'Ulic', 'name': 'Dark Ritual', 'ult': False},
    'AUdd': {'hero': 'Ulic', 'name': 'Death and Decay', 'ult': True},
    'AUim': {'hero': 'Ucrl', 'name': 'Impale', 'ult': False},
    'AUts': {'hero': 'Ucrl', 'name': 'Spiked Carapace', 'ult': False},
    'AUcb': {'hero': 'Ucrl', 'name': 'Carrion Beetles', 'ult': False},
    'AUls': {'hero': 'Ucrl', 'name': 'Locust Swarm', 'ult': True},

    'ANbf': {'hero': 'Npbm', 'name': 'Breath of Fire', 'ult': False},
    'ANdb': {'hero': 'Npbm', 'name': 'Drunken Brawler', 'ult': False},
    'ANdh': {'hero': 'Npbm', 'name': 'Drunken Haze', 'ult': False},
    'ANef': {'hero': 'Npbm', 'name': 'Storm Earth and Fire', 'ult': True},
    'ANdr': {'hero': 'Nbrn', 'name': 'Life Drain', 'ult': False},
    'ANsi': {'hero': 'Nbrn', 'name': 'Silence', 'ult': False},
    'ANba': {'hero': 'Nbrn', 'name': 'Black Arrow', 'ult': False},
    'ANch': {'hero': 'Nbrn', 'name': 'Charm', 'ult': True},
    'ANms': {'hero': 'Nngs', 'name': 'Mana Shield', 'ult': False},
    'ANfa': {'hero': 'Nngs', 'name': 'Frost Arrows', 'ult': False},
    'ANfl': {'hero': 'Nngs', 'name': 'Forked Lightning', 'ult': False},
    'ANto': {'hero': 'Nngs', 'name': 'Tornado', 'ult': True},
    'ANrf': {'hero': 'Nplh', 'name': 'Rain of Fire', 'ult': False},
    'ANca': {'hero': 'Nplh', 'name': 'Cleaving Attack', 'ult': False},
    'ANht': {'hero': 'Nplh', 'name': 'Howl of Terror', 'ult': False},
    'ANdo': {'hero': 'Nplh', 'name': 'Doom', 'ult': True},
    'ANsg': {'hero': 'Nbst', 'name': 'Summon Bear', 'ult': False},
    'ANsq': {'hero': 'Nbst', 'name': 'Summon Quilbeast', 'ult': False},
    'ANsw': {'hero': 'Nbst', 'name': 'Summon Hawk', 'ult': False},
    'ANst': {'hero': 'Nbst', 'name': 'Stampede', 'ult': True},
    'ANeg': {'hero': 'Ntin', 'name': 'Engineering Upgrade', 'ult': False},
    'ANcs': {'hero': 'Ntin', 'name': 'Cluster Rockets', 'ult': False},
    'ANc1': {'hero': 'Ntin', 'name': 'Cluster Rockets', 'ult': False},
    'ANc2': {'hero': 'Ntin', 'name': 'Cluster Rockets', 'ult': False},
    'ANc3': {'hero': 'Ntin', 'name': 'Cluster Rockets', 'ult': False},
    'ANsy': {'hero': 'Ntin', 'name': 'Pocket Factory', 'ult': False},
    'ANs1': {'hero': 'Ntin', 'name': 'Pocket Factory', 'ult': False},
    'ANs2': {'hero': 'Ntin', 'name': 'Pocket Factory', 'ult': False},
    'ANs3': {'hero': 'Ntin', 'name': 'Pocket Factory', 'ult': False},
    'ANrg': {'hero': 'Ntin', 'name': 'Robo-Goblin', 'ult': True},
    'ANg1': {'hero': 'Ntin', 'name': 'Robo-Goblin', 'ult': True},
    'ANg2': {'hero': 'Ntin', 'name': 'Robo-Goblin', 'ult': True},
    'ANg3': {'hero': 'Ntin', 'name': 'Robo-Goblin', 'ult': True},
    'ANic': {'hero': 'Nfir', 'name': 'Incinerate', 'ult': False},
    'ANia': {'hero': 'Nfir', 'name': 'Incinerate', 'ult': False},
    'ANso': {'hero': 'Nfir', 'name': 'Soul Burn', 'ult': False},
    'ANlm': {'hero': 'Nfir', 'name': 'Summon Lava Spawn', 'ult': False},
    'ANvc': {'hero': 'Nfir', 'name': 'Volcano', 'ult': True},
    'ANhs': {'hero': 'Nalc', 'name': 'Healing Spray', 'ult': False},
    'ANab': {'hero': 'Nalc', 'name': 'Acid Bomb', 'ult': False},
    'ANcr': {'hero': 'Nalc', 'name': 'Chemical Rage', 'ult': False},
    'ANtm': {'hero': 'Nalc', 'name': 'Transmute', 'ult': True}
}

tinker_dupes = {
    'ANc1': 'ANcs',
    'ANc2': 'ANcs',
    'ANc3': 'ANcs',
    'ANs1': 'ANsy',
    'ANs2': 'ANsy',
    'ANs3': 'ANsy',
    'ANg1': 'ANrg',
    'ANg2': 'ANrg',
    'ANg3': 'ANrg'
}

upgrade_codes = {
    'Rhss': {'name': 'Control Magic', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Control Magic', 'gold': 75, 'wood': 75}]},
    'Rhme': {'name': 'Human Melee Attack', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Iron Forged Swords', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Steel Forged Swords', 'gold': 175, 'wood': 175}, {'level': 3, 'name': 'Mithril Forged Swords', 'gold': 250, 'wood': 300}]},
    'Rhra': {'name': 'Human Ranged Attack', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Black Gunpowder', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Refined Gunpowder', 'gold': 175, 'wood': 175}, {'level': 3, 'name': 'Imbued Gunpowder', 'gold': 250, 'wood': 300}]},
    'Rhar': {'name': 'Human Melee Armor', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Iron Plating', 'gold': 125, 'wood': 75}, {'level': 2, 'name': 'Steel Plating', 'gold': 150, 'wood': 175}, {'level': 3, 'name': 'Mithril Plating', 'gold': 175, 'wood': 275}]},
    'Rhla': {'name': 'Human Ranged Armor', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Studded Leather Armor', 'gold': 100, 'wood': 100}, {'level': 2, 'name': 'Reinforced Leather Armor', 'gold': 150, 'wood': 175}, {'level': 3, 'name': 'Dragonhide Armor', 'gold': 200, 'wood': 250}]},
    'Rhac': {'name': 'Masonry', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Improved Masonry', 'gold': 125, 'wood': 50}, {'level': 2, 'name': 'Advanced Masonry', 'gold': 150, 'wood': 75}, {'level': 2, 'name': 'Imbued Masonry', 'gold': 175, 'wood': 100}]},
    'Rhgb': {'name': 'Flying Machine Bombs', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Flying Machine Bombs', 'gold': 150, 'wood': 100}]},
    'Rhlh': {'name': 'Lumber Harvesting', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Improved Lumber Harvesting', 'gold': 100, 'wood': 0}, {'level': 2, 'name': 'Advanced Lumber Harvesting', 'gold': 200, 'wood': 0}]},
    'Rhde': {'name': 'Defend', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Defend', 'gold': 150, 'wood': 100}]},
    'Rhan': {'name': 'Animal War Training', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Animal War Training', 'gold': 125, 'wood': 125}]},
    'Rhpt': {'name': 'Priest Training', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Priest Adept Training', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Priest Master Training', 'gold': 100, 'wood': 150}]},
    'Rhst': {'name': 'Sorceress Training', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Sorceress Adept Training', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Sorceress Master Training', 'gold': 100, 'wood': 150}]},
    'Rhri': {'name': 'Long Rifles', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Long Rifles', 'gold': 75, 'wood': 125}]},
    'Rhse': {'name': 'Magic Sentry', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Magic Sentry', 'gold': 50, 'wood': 50}]},
    'Rhfl': {'name': 'Flare', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Flare', 'gold': 50, 'wood': 50}]},
    'Rhhb': {'name': 'Storm Hammers', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Storm Hammers', 'gold': 125, 'wood': 225}]},
    'Rhrt': {'name': 'Barrage', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Barrage', 'gold': 50, 'wood': 150}]},
    'Rhpm': {'name': 'Backpack', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Backpack', 'gold': 50, 'wood': 25}]},
    'Rhfc': {'name': 'Flak Cannons', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Flak Cannons', 'gold': 100, 'wood': 150}]},
    'Rhfs': {'name': 'Fragmentation Shards', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Fragmentation Shards', 'gold': 50, 'wood': 100}]},
    'Rhcd': {'name': 'Cloud', 'race': 'H', 'levels':  [{'level': 1, 'name': 'Cloud', 'gold': 50, 'wood': 100}]},
    'Rhsb': {'name': 'Sundering Blades', 'race': 'H', 'levels': [{'level': 1, 'name': 'Sundering Blades', 'gold': 100, 'wood': 100}]},

    'Rome': {'name': 'Orc Melee Attack', 'race': 'O', 'levels': [{'level': 1, 'name': 'Steel Melee Weapons', 'gold': 100, 'wood': 75}, {'level': 2, 'name': 'Thorium Melee Weapons', 'gold': 150, 'wood': 175}, {'level': 3, 'name': 'Arcanite Melee Weapons', 'gold': 200, 'wood': 275}]},
    'Rora': {'name': 'Orc Ranged Attack', 'race': 'O', 'levels': [{'level': 1, 'name': 'Steel Ranged Weapons', 'gold': 100, 'wood': 100}, {'level': 2, 'name': 'Thorium Ranged Weapons', 'gold': 150, 'wood': 200}, {'level': 3, 'name': 'Arcanite Ranged Weapons', 'gold': 200, 'wood': 300}]},
    'Roar': {'name': 'Orc Armor', 'race': 'O', 'levels': [{'level': 1, 'name': 'Steel Armor', 'gold': 150, 'wood': 75}, {'level': 2, 'name': 'Thorium Armor', 'gold': 225, 'wood': 225}, {'level': 3, 'name': 'Arcanite Armor', 'gold': 300, 'wood': 375}]},
    'Rwdm': {'name': 'War Drums Damage Increase', 'race': 'O', 'levels': [{'level': 1, 'name': 'War Drums Damage Increase', 'gold': 100, 'wood': 150}]},
    'Ropg': {'name': 'Pillage', 'race': 'O', 'levels': [{'level': 1, 'name': 'Pillage', 'gold': 75, 'wood': 25}]},
    'Robs': {'name': 'Berserker Strength', 'race': 'O', 'levels': [{'level': 1, 'name': 'Berserker Strength', 'gold': 50, 'wood': 150}]},
    'Rows': {'name': 'Pulverize', 'race': 'O', 'levels': [{'level': 1, 'name': 'Pulverize', 'gold': 100, 'wood': 250}]},  # Todo: verify that this is correct post-1.30
    'Roen': {'name': 'Ensnare', 'race': 'O', 'levels': [{'level': 1, 'name': 'Ensnare', 'gold': 50, 'wood': 75}]},
    'Rovs': {'name': 'Envenomed Spears', 'race': 'O', 'levels': [{'level': 1, 'name': 'Envenomed Spears', 'gold': 100, 'wood': 150}]},
    'Rowd': {'name': 'Witch Doctor Training', 'race': 'O', 'levels': [{'level': 1, 'name': 'Witch Doctor Adept Training', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Witch Doctor Master Training', 'gold': 100, 'wood': 150}]},
    'Rost': {'name': 'Shaman Training', 'race': 'O', 'levels': [{'level': 1, 'name': 'Shaman Adept Training', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Shaman Master Training', 'gold': 100, 'wood': 150}]},
    'Rosp': {'name': 'Spiked Barricades', 'race': 'O', 'levels': [{'level': 1, 'name': 'Spiked Barricades', 'gold': 25, 'wood': 75}, {'level': 2, 'name': 'Improved Spiked Barricades', 'gold': 50, 'wood': 100}]},
    'Rotr': {'name': 'Troll Regeneration', 'race': 'O', 'levels': [{'level': 1, 'name': 'Troll Regeneration', 'gold': 100, 'wood': 100}]},
    'Rolf': {'name': 'Liquid Fire', 'race': 'O', 'levels': [{'level': 1, 'name': 'Liquid Fire', 'gold': 75, 'wood': 125}]},
    'Ropm': {'name': 'Backpack', 'race': 'O', 'levels': [{'level': 1, 'name': 'Backpack', 'gold': 50, 'wood': 25}]},
    'Rowt': {'name': 'Spirit Walker Training', 'race': 'O', 'levels': [{'level': 1, 'name': 'Spirit Walker Adept Training', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Spirit Walker Master Training', 'gold': 100, 'wood': 150}]},
    'Robk': {'name': 'Berserker Upgrade', 'race': 'O', 'levels': [{'level': 1, 'name': 'Berserker Upgrade', 'gold': 75, 'wood': 175}]},
    'Rorb': {'name': 'Reinforced Defenses', 'race': 'O', 'levels': [{'level': 1, 'name': 'Reinforced Defenses', 'gold': 75, 'wood': 175}]},
    'Robf': {'name': 'Burning Oil', 'race': 'O', 'levels': [{'level': 1, 'name': 'Burning Oil', 'gold': 50, 'wood': 150}]},

    'Resm': {'name': 'Strength of the Moon', 'race': 'N', 'levels': [{'level': 1, 'name': 'Strength of the Moon', 'gold': 125, 'wood': 75}, {'level': 2, 'name': 'Improved Strength of the Moon', 'gold': 175, 'wood': 175}, {'level': 3, 'name': 'Advanced Strength of the Moon', 'gold': 225, 'wood': 275}]},
    'Resw': {'name': 'Strength of the Wild', 'race': 'N', 'levels': [{'level': 1, 'name': 'Strength of the Wild', 'gold': 100, 'wood': 75}, {'level': 2, 'name': 'Improved Strength of the Wild', 'gold': 175, 'wood': 175}, {'level': 3, 'name': 'Advanced Strength of the Wild', 'gold': 250, 'wood': 275}]},
    'Rema': {'name': 'Moon Armor', 'race': 'N', 'levels': [{'level': 1, 'name': 'Moon Armor', 'gold': 150, 'wood': 75}, {'level': 2, 'name': 'Improved Moon Armor', 'gold': 200, 'wood': 150}, {'level': 3, 'name': 'Advanced Moon Armor', 'gold': 250, 'wood': 225}]},
    'Rerh': {'name': 'Reinforced Hides', 'race': 'N', 'levels': [{'level': 1, 'name': 'Reinforced Hides', 'gold': 150, 'wood': 50}, {'level': 2, 'name': 'Improved Reinforced Hides', 'gold': 200, 'wood': 150}, {'level': 3, 'name': 'Advanced Reinforced Hides', 'gold': 250, 'wood': 250}]},
    'Reuv': {'name': 'Ultravision', 'race': 'N', 'levels': [{'level': 1, 'name': 'Ultravision', 'gold': 50, 'wood': 50}]},
    'Renb': {'name': "Nature's Blessing", 'race': 'N', 'levels': [{'level': 1, 'name': "Nature's Blessing", 'gold': 150, 'wood': 200}]},
    'Reib': {'name': 'Improved Bows', 'race': 'N', 'levels': [{'level': 1, 'name': 'Improved Bows', 'gold': 50, 'wood': 100}]},
    'Remk': {'name': 'Marksmanship', 'race': 'N', 'levels': [{'level': 1, 'name': 'Marksmanship', 'gold': 100, 'wood': 175}]},
    'Resc': {'name': 'Sentinel', 'race': 'N', 'levels': [{'level': 1, 'name': 'Sentinel', 'gold': 100, 'wood': 100}]},
    'Remg': {'name': 'Upgrade Moon Glaive', 'race': 'N', 'levels': [{'level': 1, 'name': 'Moon Glaive', 'gold': 100, 'wood': 150}]},
    'Redt': {'name': 'Druid of the Talon Training', 'race': 'N', 'levels': [{'level': 1, 'name': 'Druid of the Talon Adept Training', 'gold':100 , 'wood': 50}, {'level': 2, 'name': 'Druid of the Talon Master Training', 'gold': 100, 'wood': 150}]},
    'Redc': {'name': 'Druid of the Claw Training', 'race': 'N', 'levels': [{'level': 1, 'name': 'Druid of the Claw Adept Training', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Druid of the Claw Master Training', 'gold': 100, 'wood': 150}]},
    'Resi': {'name': 'Abolish Magic', 'race': 'N', 'levels': [{'level': 1, 'name': 'Abolish Magic', 'gold': 50, 'wood': 50}]},
    'Reht': {'name': 'Hippogryph Taming', 'race': 'N', 'levels': [{'level': 1, 'name': 'Hippogryph Taming', 'gold': 75, 'wood': 75}]},
    'Recb': {'name': 'Corrosive Breath', 'race': 'N', 'levels': [{'level': 1, 'name': 'Corrosive Breath', 'gold': 125, 'wood': 225}]},
    'Repb': {'name': 'Vorpal Blades', 'race': 'N', 'levels': [{'level': 1, 'name': 'Vorpal Blades', 'gold': 125, 'wood': 100}]},
    'Rers': {'name': 'Resistant Skin', 'race': 'N', 'levels': [{'level': 1, 'name': 'Resistant Skin', 'gold': 50, 'wood': 100}]},
    'Rehs': {'name': 'Hardened Skin', 'race': 'N', 'levels': [{'level': 1, 'name': 'Hardened Skin', 'gold': 100, 'wood': 175}]},
    'Reeb': {'name': 'Mark of the Claw', 'race': 'N', 'levels': [{'level': 1, 'name': 'Mark of the Claw', 'gold': 25, 'wood': 100}]},
    'Reec': {'name': 'Mark of the Talon', 'race': 'N', 'levels': [{'level': 1, 'name': 'Mark of the Talon', 'gold': 100, 'wood': 50}]},
    'Rews': {'name': 'Well Spring', 'race': 'N', 'levels': [{'level': 1, 'name': 'Well Spring', 'gold': 75, 'wood': 150}]},
    'Repm': {'name': 'Backpack', 'race': 'N', 'levels': [{'level': 1, 'name': 'Backpack', 'gold': 50, 'wood': 25}]},
    'Roch': {'name': 'Chaos', 'race': 'N', 'levels': [{'level': 1, 'name': 'Unknown', 'gold': 0, 'wood': 0}]},  # Todo: what is this

    'Rusp': {'name': 'Destroyer Form', 'race': 'U', 'levels': [{'level': 1, 'name': 'Destroyer Form', 'gold': 75, 'wood': 150}]},
    'Rume': {'name': 'Unholy Strength', 'race': 'U', 'levels': [{'level': 1, 'name': 'Unholy Strength', 'gold': 125, 'wood': 50}, {'level': 2, 'name': 'Improved Unholy Strength', 'gold': 200, 'wood': 150}, {'level': 3, 'name': 'Advanced Unholy Strength', 'gold': 275, 'wood': 250}]},
    'Rura': {'name': 'Creature Attack', 'race': 'U', 'levels': [{'level': 1, 'name': 'Creature Attack', 'gold': 150, 'wood': 50}, {'level': 2, 'name': 'Improved Creature Attack', 'gold': 200, 'wood': 125}, {'level': 3, 'name': 'Advanced Creature Attack', 'gold': 250, 'wood': 200}]},
    'Ruar': {'name': 'Unholy Armor', 'race': 'U', 'levels': [{'level': 1, 'name': 'Unholy Armor', 'gold': 125, 'wood': 50}, {'level': 2, 'name': 'Improved Unholy Armor', 'gold': 200, 'wood': 150}, {'level': 3, 'name': 'Advanced Unholy Armor', 'gold': 275, 'wood': 250}]},
    'Rucr': {'name': 'Creature Carapace', 'race': 'U', 'levels': [{'level': 1, 'name': 'Creature Carapace', 'gold': 150, 'wood': 75}, {'level': 2, 'name': 'Improved Creature Carapace', 'gold': 200, 'wood': 200}, {'level': 3, 'name': 'Advanced Creature Carapace', 'gold': 250, 'wood': 325}]},
    'Ruac': {'name': 'Cannibalize', 'race': 'U', 'levels': [{'level': 1, 'name': 'Cannibalize', 'gold': 75, 'wood': 0}]},
    'Rugf': {'name': 'Ghoul Frenzy', 'race': 'U', 'levels': [{'level': 1, 'name': 'Ghoul Frenzy', 'gold': 100, 'wood': 150}]},
    'Ruwb': {'name': 'Web', 'race': 'U', 'levels': [{'level': 1, 'name': 'Web', 'gold': 150, 'wood':150}]},
    'Rusf': {'name': 'Stone Form', 'race': 'U', 'levels': [{'level': 1, 'name': 'Stone Form', 'gold': 75, 'wood': 150}]},
    'Rune': {'name': 'Necromancer Training', 'race': 'U', 'levels': [{'level': 1, 'name': 'Necromancer Adept Training', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Necromancer Master Training', 'gold': 100, 'wood': 150}]},
    'Ruba': {'name': 'Banshee Training', 'race': 'U', 'levels': [{'level': 1, 'name': 'Banshee Adept Training', 'gold': 100, 'wood': 50}, {'level': 2, 'name': 'Banshee Master Training', 'gold': 100, 'wood': 150}]},
    'Rufb': {'name': 'Freezing Breath', 'race': 'U', 'levels': [{'level': 1, 'name': 'Freezing Breath', 'gold': 150, 'wood': 275}]},
    'Rusl': {'name': 'Skeletal Longevity', 'race': 'U', 'levels': [{'level': 1, 'name': 'Skeletal Longevity', 'gold': 0, 'wood': 0}]},
    'Rupc': {'name': 'Disease Cloud', 'race': 'U', 'levels': [{'level': 1, 'name': 'Disease Cloud', 'gold': 100, 'wood': 200}]},
    'Rusm': {'name': 'Skeletal Mastery', 'race': 'U', 'levels': [{'level': 1, 'name': 'Skeletal Mastery', 'gold': 200, 'wood': 175}]},
    'Rubu': {'name': 'Burrow', 'race': 'U', 'levels': [{'level': 1, 'name': 'Burrow', 'gold': 75, 'wood': 75}]},
    'Ruex': {'name': 'Exhume Corpses', 'race': 'U', 'levels': [{'level': 1, 'name': 'Exhume Corpses', 'gold': 75, 'wood': 50}]},
    'Rupm': {'name': 'Backpack', 'race': 'U', 'levels': [{'level': 1, 'name': 'Backpack', 'gold': 50, 'wood': 25}]}
}

neutral_codes = {
    'ngol': 'Gold Mine',
    'ntav': 'Tavern',
    'ngme': 'Goblin Merchant',
    'ngad': 'Goblin Laboratory',
    'nmer': 'Mercenary Camp (Lordaeron Summer)',
    'nmr0': 'Mercenary Camp (Village)',
    'nmr2': 'Mercenary Camp (Lordaeron Fall)',
    'nmr3': 'Mercenary Camp (Lordaeron Winter)',
    'nmr4': 'Mercenary Camp (Barrens)',
    'nmr5': 'Mercenary Camp (Ashenvale)',
    'nmr6': 'Mercenary Camp (Felwood)',
    'nmr7': 'Mercenary Camp (Northrend)',
    'nmr8': 'Mercenary Camp (Cityscape)',
    'nmr9': 'Mercenary Camp (Dalaran)',
    'nmra': 'Mercenary Camp (Dungeon)',
    'nmrb': 'Mercenary Camp (Underground)',
    'nmrc': 'Mercenary Camp (Sunken Ruins)',
    'nmrd': 'Mercenary Camp (Icecrown Glacier)',
    'nmre': 'Mercenary Camp (Outland)',
    'nmrf': 'Mercenary Camp (Black Citadel)',
    'ndrk': 'Black Dragon Roost',
    'ndru': 'Blue Dragon Roost',
    'ndrz': 'Bronze Dragon Roost',
    'ndrg': 'Green Dragon Roost',
    'ndro': 'Nether Dragon Roost',
    'ndrr': 'Red Dragon Roost',
    'nmrk': 'Marketplace',
    'nfoh': 'Fountain of Health',
    'nmoo': 'Fountain of Mana',
    'bDNR': 'Random Fountain',
    'nwgt': 'Way Gate'
}

level_exp = {
    1: 25,
    2: 40,
    3: 60,
    4: 85,
    5: 115,
    6: 150,
    7: 190,
    8: 235,
    9: 285,
    10: 340
}

preempt_versions = ['1.33']     # game versions that did not increment the buildNo

build_versions = {
    '6114': '1.32.10',   # 2020-04-14, lumber and itemsell buff
    '6112': '1.32.9',    # 2020-10-21, broad balance changes
    '6111': '1.32.8',    # 2020-08-11, beetle unbuff, FFA name obfuscation
    '6110': '1.32.6 / 1.32.7',   # 2020-06-02, balancing: beetle buff, item changes, merc changes. no buildNo change for 1.32.7
    '6109': '1.32.4 / 1.32.5',   # 2020-04-28, reforged graphics tuning, desync fixes, banewood readded again. no buildNo change for 1.32.5
    '6108': '1.32.3',   # 2020-03-18, desync fixes, strath/banewood/foundtain readded
    '6106': '1.32.2',   # 2020-02-24, minor bugfixes, removal of strath/banewood/fountain
    '6105': '1.32 / 1.32.1',     # 2020-01-28, launch version. no buildNo change for 1.32.1 (2020-02-06, minor bugfixes)
    '6103': '1.32.0.6', # 2020-01-17, classic camera fix
    '6102': '1.32.0.5', # 2020-01-09, adds classic gfx
    '6098': '1.32.0.4', # 2019-12-09, adds customs and mappool
    '6094': '1.32.0.3 / 1.32.0.3.1', # 2019-11-20, adds NE/random. no buildNo change for 1.32.0.3.1 (2019-12-03, adds collections)
    '6092': '1.32.0.2 / 1.32.0.2.1', # 2019-11-05, adds UD. no buildNo change for 1.32.0.2.1 (2019-11-13, adds 3s/4s/ffa)
    '6091': '1.32.0.1'  # 2019-10-29, first beta build
}

""" The full set of flags are just here as error handling for custom games.
    The ally event functions in the Replay model only properly handle share/unshare,
    and the replay.html template only renders share/unshare events.
    The flags marked with (?) haven't been directly tested.
    For the bitwise diagram: W = allied victory, C = control, V = vision, A = ally """
ally_event_codes = {        #                                           W...CVAAAAA
    1151: 'share',          # ally, share vision, share control         10001111111
    1087: 'unshare',        # ally, share vision, no control            10000111111
    1056: 'enemyvision',    # unally, share vision, no control          10000100000
    1055: 'unvision',       # ally, no vision, no control (?)           10000011111
    1119: 'blindshare',     # ally, no vision, share control (?)        10001011111
    1024: 'unally',         # unally, no vision, no control? (?)        10000000000
    127:  'novictoryally',  # no alliedvictory, ally, vis/ctrl (?)      00001111111
    31:   'weakally',       # no alliedvictory, ally, no vis/ctrl (?)   00000011111
    0:    'unweakally'      # no alliedvictory, unally, no vis/ctrl (?) 00000000000
}

is_tower = {'hwtw', 'owtw', 'etrp'}

is_tower_upgrade = {'hgtw', 'hatw', 'hctw', 'uzg1', 'uzg2'}

is_worker = {'hpea', 'opeo', 'ewsp', 'uaco'}

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

player_colors = {
    0: '#ff0303',
    1: '#0042ff',
    2: '#1ce6b9',
    3: '#540081',
    4: '#fffc00',
    5: '#fe8a0e',
    6: '#20c000',
    7: '#e55bb0',
    8: '#959697',
    9: '#7ebff1',
    10: '#106246',
    11: '#4a2a04',
    12: '#9b0000',
    13: '#0000c3',
    14: '#00eaff',
    15: '#be00fe',
    16: '#ebcd87',
    17: '#f8a48b',
    18: '#bfff80',
    19: '#dcb9eb',
    20: '#282828',
    21: '#ebf0ff',
    22: '#00781e',
    23: '#a46f33'
}


# Todo: move to a models/map when we create the map details

all_map_info = None


def get_all_mapinfo(fp=None):
    global all_map_info
    if all_map_info is None:
        gp = fp.get_path if fp else get_path
        with open(gp('resource/mapinfo.json'), 'r') as f:
            all_map_info = json.load(f)
    return all_map_info


def get_mapinfo(map_name, fp=None):
    mapinfo = get_all_mapinfo(fp)
    if map_name not in mapinfo:
        return None
    return mapinfo[map_name]


def get_map_size(map_name, fp=None):
    map_info = get_mapinfo(map_name, fp)
    if not map_info:
        return None
        
    x = map_info['x']
    y = map_info['y']
    return [x[0], x[1], y[0], y[1]]


def get_starting_locations(map_name, fp=None, simple=True):
    map_info = get_mapinfo(map_name, fp)
    if not map_info:
        return None
    if simple:
        return [[location['x'], location['y']] for location in map_info['starts']]
    return map_info['starts']


def get_goldmines(map_name, fp=None):
    map_info = get_mapinfo(map_name, fp)
    if not map_info or 'mines' not in map_info:
        return None

    return map_info['mines']


def get_neutral_buildings(map_name, fp=None):
    map_info = get_mapinfo(map_name, fp)
    if not map_info or 'neutral_buildings' not in map_info:
        return None

    return map_info['neutral_buildings']


def get_map_creep_camps(map_name, fp=None):
    map_info = get_mapinfo(map_name, fp)
    if not map_info or 'creepCamps' not in map_info:
        return None

    return map_info['creepCamps']


def get_map_creep_totals(map_name, fp=None):
    map_info = get_mapinfo(map_name, fp)
    if not map_info or 'creepCamps' not in map_info:
        return None

    total_camps = 0
    total_creeps = 0
    total_exp = 0

    for camp in map_info['creepCamps']:
        total_camps += 1
        for creep in camp['creeps']:
            total_creeps += creep['count']
            total_exp += level_exp[creep_codes[creep['id']]['level']] * creep['count']

    return {'camps': total_camps, 'creeps': total_creeps, 'exp': total_exp}


def get_map_critters(map_name, fp=None):
    map_info = get_mapinfo(map_name, fp)
    if not map_info or 'critters' not in map_info:
        return None

    return map_info['critters']

map_translations = {
    'w3c_ffa_anarchycastle_anon': '(4)AnarchyCastle',
    'w3c_ffa_deadlock lv_anon': '(8)Deadlock',
    'w3c_ffa_deathrose_anon': '(8)Deathrose',
    'w3c_ffa_ferocity_anon': '(8)Ferocity',
    'w3c_ffa_fountainofmanipulation_anon': '(4)FountainOfManipulation',
    'w3c_ffa_frozenmarshlands_anon': '(4)FrozenMarshlands',
    'w3c_ffa_harvestofsorrow_anon': '(6)HarvestOfSorrow',
    'w3c_ffa_marketsquare_anon': '(8)MarketSquare',
    'w3c_ffa_neoncity_anon': '(6)NeonCity',
    'w3c_ffa_rockslide_anon': '(6)Rockslide',
    'w3c_ffa_sanctuary lv_anon': '(8)Sanctuary_LV',
    'w3c_ffa_silverpineforest_anon': '(6)SilverpineForest',
    'w3c_ffa_tatsascastlegardens_anon': '(8)TatsasCastleGardens',
    'w3c_ffa_twilightruins_anon': '(8)TwilightRuins_LV',

    'w3c_1v1_amazonia_anon': '(2)Amazonia',
    'w3c_1v1_autumnleaves_anon': '(2)AutumnLeaves',
    'w3c_1v1_autumn_leaves_201016': '(2)AutumnLeaves',
    'w3c_1v1_concealedhill_anon': '(2)ConcealedHill',
    'w3c_1v1_echoisles_anon': '(2)EchoIsles',
    'w3c_1v1_lastrefuge_anon': '(2)LastRefuge',
    'w3c_1v1_lastrefuge.anon': '(2)LastRefuge',
    'w3c_1v1_northernisles_anon': '(2)NorthernIsles',
    'w3c_1v1_terenasstand_lv_anon': '(2)TerenasStand_LV',
    'w3c_1v1_twistedmeadows_anon': '(2)TwistedMeadows',
    
    'w3c_avalanche_lv_anon': '(4)Avalanche',
    'w3c_battlegrounds_anon': '(8)Battleground_LV',
    'w3c_cherryville_anon': '(8)Cherryville',
    'w3c_circleoffallenheroes_anon': '(5)CircleOfFallenHeroes',
    'w3c_deadlock_lv_anon': '(8)Deadlock_LV',
    'w3c_dragonfalls_anon': '(8)DragonFalls',
    'w3c_feralas_lv_anon': '(8)Feralas_LV',
    'w3c_fullscaleassault_anon': '(8)FullScaleAssault',
    'w3c_gnollwood_anon': '(6)GnollWood',
    'w3c_goldrush_anon': '(8)GoldRush',
    'w3c_goldshire_anon': '(4)Goldshire',
    'w3c_goleminthemist_lv_anon': '(8)GolemsInTheMist_LV',
    'w3c_hillsbradcreek_anon': '(4)HillsbradCreek',
    'w3c_losttemple_lv_anon': '(4)LostTemple_LV',
    'w3c_marketsquare_anon': '(8)MarketSquare',
    "w3c_mur'galoasis_lv_anon": "(8)Mur'gulOasis_LV",
    'w3c_nerubianpassage_anon': '(8)NerubianPassage',
    'w3c_northernfelwood_anon': '(8)NorthernFelwood',
    'w3c_northshire_lv_anon': '(8)Northshire_LV',
    'w3c_sanctuary_lv_anon': '(8)Sanctuary_LV',
    'w3c_tidewaterglades_lv_anon': '(4)TidewaterGlades_LV',
    'w3c_turtlerock_anon': '(4)TurtleRock',
    'w3c_twilightruins_lv_anon': '(8)TwilightRuins_LV',
    'w3c_twilightruins_lv': '(8)TwilightRuins_LV'
}

def get_map_canonical_name(map_name, fp=None):
    """The canonical map filename, e.g. '(6)Highperch'
       This is mostly to help with custom-hosted game replays
       lowercasing the map filenames for some reason
       Also w3champions support since they mangled all the map names"""
    if map_name.lower() in map_translations:
        return map_translations[map_name.lower()]
    canonical_names = get_all_mapinfo(fp=fp).keys()
    if map_name in canonical_names:
        return map_name
    for canonical in canonical_names:
        if map_name.lower() == canonical.lower():
            return canonical
    return map_name     # we didn't find one


map_untranslations = {translated: untranslated for untranslated, translated in map_translations.items()}

def untranslate_map_name(map_name):
    if map_name in map_untranslations:
        return map_untranslations[map_name]
    return map_name


def get_map_title(map_name):
    """The map's title as chosen by the map creator
       and saved in the info file inside the map archive
       e.g. 'Terenas Stand LV' """
    return get_mapinfo(map_name)['mapTitle']