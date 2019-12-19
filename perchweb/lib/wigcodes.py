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

item_codes = {
    "stwp": {"name": "Scroll of Town Portal", "table": "shop", "shop": "ambiguous", "price": 350},
    "dust": {"name": "Dust of Appearance", "table": "shop", "shop": "ambiguous", "price": 75},
    "shea": {"name": "Scroll of Healing", "table": "shop", "shop": "ambiguous", "price": 250},

    "plcl": {"name": "Lesser Clarity Potion", "table": "shop", "shop": "race_all", "price": 70},
    "phea": {"name": "Potion of Healing", "table": "shop", "shop": "race_all", "price": 150},
    "pman": {"name": "Potion of Mana", "table": "shop", "shop": "race_all", "price": 200},

    "ofir": {"name": "Orb of Fire", "table": "shop", "shop": "race_H", "price": 325},
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

    "spsh": {"name": "Amulet of Spell Shield", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "rhth": {"name": "Khadgar's Gem of Health", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "odef": {"name": "Orb of Darkness", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "pmna": {"name": "Pendant of Mana", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "rde4": {"name": "Ring of Protection +5", "table": "perm_L6", "shop": "marketplace", "price": 600},
    "ssil": {"name": "Staff of Silence", "table": "perm_L6", "shop": "marketplace", "price": 600},

    "ratf": {"name": "Claws of Attack +15", "table": "artifact_L7", "shop": "marketplace", "price": 800},
    "desc": {"name": "Kelen's Dagger of Escape", "table": "artifact_L7", "shop": "marketplace", "price": 800},
    "ofro": {"name": "Orb of Frost", "table": "artifact_L7", "shop": "marketplace", "price": 800},

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
    "fgrd": {"name": "Red Drake Egg", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "sres": {"name": "Scroll of Restoration", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "fgfh": {"name": "Spiked Collar", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "fgrg": {"name": "Stone Token", "table": "charged_L5", "shop": "marketplace", "price": 550},
    "totw": {"name": "Talisman of the Wild", "table": "charged_L5", "shop": "marketplace", "price": 550},

    "wild": {"name": "Amulet of the Wild", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "fgdg": {"name": "Demonic Figurine", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "shar": {"name": "Ice Shard", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "infs": {"name": "Inferno Stone", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "sand": {"name": "Scroll of Animate Dead", "table": "charged_L6", "shop": "marketplace", "price": 700},
    "srrc": {"name": "Scroll of Resurrection", "table": "charged_L6", "shop": "marketplace", "price": 700},

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

    map_name = map_name.lower()
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

    map_name = map_name.lower()
    if map_name not in map_info:
        return None
    return map_info[map_name]['start']
