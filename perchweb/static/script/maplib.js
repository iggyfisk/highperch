const neutralBuildingCodes = {
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
};

const creepCodes = {
    "nahy": {
        "name": "Ancient Hydra",
        "level": 10,
        "hp": 1600,
        "mana": 600
    },
    "nsqa": {
        "name": "Ancient Sasquatch",
        "level": 9,
        "hp": 1200,
        "mana": 600
    },
    "nwna": {
        "name": "Ancient Wendigo",
        "level": 9,
        "hp": 1200,
        "mana": 600
    },
    "nwiz": {
        "name": "Apprentice Wizard",
        "level": 1,
        "hp": 180
    },
    "nane": {
        "name": "Arachnathid Earth-Borer",
        "level": 4,
        "hp": 400,
        "mana": 200
    },
    "nano": {
        "name": "Overlord Arachnathid",
        "level": 5,
        "hp": 750
    },
    "nanw": {
        "name": "Warrior Arachnathid",
        "level": 3,
        "hp": 375
    },
    "nass": {
        "name": "Assassin",
        "level": 4,
        "hp": 450
    },
    "nban": {
        "name": "Bandit",
        "level": 1,
        "hp": 240
    },
    "nbld": {
        "name": "Bandit Lord",
        "level": 7,
        "hp": 950,
        "mana": 500
    },
    "nanb": {
        "name": "Barbed Arachnathid",
        "level": 1,
        "hp": 200
    },
    "nanm": {
        "name": "Barbed Arachnathid",
        "level": 1,
        "hp": 200
    },
    "narg": {
        "name": "Battle Golem",
        "level": 3,
        "hp": 500
    },
    "nelb": {
        "name": "Berserk Elemental",
        "level": 8,
        "hp": 1100,
        "mana": 500
    },
    "nowk": {
        "name": "Berserk Wildkin",
        "level": 8,
        "hp": 1100,
        "mana": 500
    },
    "nbwm": {
        "name": "Black Dragon",
        "level": 10,
        "hp": 2200
    },
    "nbdr": {
        "name": "Black Dragon Whelp",
        "level": 3,
        "hp": 340
    },
    "nbdk": {
        "name": "Black Drake",
        "level": 6,
        "hp": 950
    },
    "nspb": {
        "name": "Black Spider",
        "level": 1,
        "hp": 240
    },
    "nfgb": {
        "name": "Bloodfiend",
        "level": 4,
        "hp": 450
    },
    "nadr": {
        "name": "Blue Dragon",
        "level": 10,
        "hp": 2200
    },
    "nadw": {
        "name": "Blue Dragon Whelp",
        "level": 3,
        "hp": 340
    },
    "nbda": {
        "name": "Blue Dragonspawn Apprentice",
        "level": 4,
        "hp": 350,
        "mana": 250
    },
    "nbdm": {
        "name": "Blue Dragonspawn Meddler",
        "level": 3,
        "hp": 500
    },
    "nbdo": {
        "name": "Blue Dragonspawn Overseer",
        "level": 8,
        "hp": 1000,
        "mana": 400
    },
    "nbds": {
        "name": "Blue Dragonspawn Sorceror",
        "level": 6,
        "hp": 675,
        "mana": 400
    },
    "nbdw": {
        "name": "Blue Dragonspawn Warrior",
        "level": 5,
        "hp": 775
    },
    "nadk": {
        "name": "Blue Drake",
        "level": 6,
        "hp": 950
    },
    "nbrg": {
        "name": "Brigand",
        "level": 2,
        "hp": 300
    },
    "nbzd": {
        "name": "Bronze Dragon",
        "level": 10,
        "hp": 2200
    },
    "nbzw": {
        "name": "Bronze Dragon Whelp",
        "level": 3,
        "hp": 340
    },
    "nbzk": {
        "name": "Bronze Drake",
        "level": 6,
        "hp": 950
    },
    "nsbm": {
        "name": "Brood Mother",
        "level": 6,
        "hp": 750
    },
    "nskf": {
        "name": "Burning Archer",
        "level": 3,
        "traits": "Undead",
        "hp": 300,
        "mana": 300
    },
    "ncer": {
        "name": "Centaur Drudge",
        "level": 2,
        "hp": 300
    },
    "ncim": {
        "name": "Centaur Impaler",
        "level": 4,
        "hp": 350,
        "mana": 200
    },
    "ncnk": {
        "name": "Centaur Khan",
        "level": 8,
        "hp": 900,
        "mana": 500
    },
    "ncen": {
        "name": "Centaur Outrunner",
        "level": 4,
        "hp": 550
    },
    "ncks": {
        "name": "Centaur Sorceror",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "ncea": {
        "name": "Centaurarcher",
        "level": 2,
        "hp": 300
    },
    "nenc": {
        "name": "Corrupted Treant",
        "level": 1,
        "hp": 240
    },
    "nanc": {
        "name": "Crystal Arachnathid",
        "level": 1,
        "hp": 200
    },
    "ndmu": {
        "name": "Dalaran Mutant",
        "level": 2,
        "hp": 330
    },
    "ndrj": {
        "name": "Dalaran Reject",
        "level": 1,
        "hp": 240
    },
    "ndtb": {
        "name": "Dark Troll Berserker",
        "level": 4,
        "hp": 450
    },
    "ndth": {
        "name": "Dark Troll High Priest",
        "level": 4,
        "hp": 450,
        "mana": 300
    },
    "ndtp": {
        "name": "Dark Troll Shadow Priest",
        "level": 2,
        "hp": 240,
        "mana": 200
    },
    "nwzd": {
        "name": "Dark Wizard",
        "level": 8,
        "hp": 1200,
        "mana": 500
    },
    "ndtr": {
        "name": "Dark Troll",
        "level": 2,
        "hp": 300
    },
    "ndtt": {
        "name": "Dark Troll Trapper",
        "level": 3,
        "hp": 340
    },
    "ndtw": {
        "name": "Dark Troll Warlord",
        "level": 6,
        "hp": 750
    },
    "nrvd": {
        "name": "Death Revenant",
        "level": 9,
        "traits": "Undead",
        "hp": 1500,
        "mana": 600
    },
    "nhdc": {
        "name": "Deceiver",
        "level": 3,
        "hp": 300,
        "mana": 300
    },
    "nlrv": {
        "name": "Deeplord Revenant",
        "level": 10,
        "traits": "Undead",
        "hp": 2100,
        "mana": 600
    },
    "nwwd": {
        "name": "Dire Frost Wolf",
        "level": 6,
        "hp": 750,
        "mana": 400
    },
    "nmdr": {
        "name": "Dire Mammoth",
        "level": 8,
        "hp": 1550
    },
    "nwld": {
        "name": "Dire Wolf",
        "level": 6,
        "hp": 750,
        "mana": 400
    },
    "nbal": {
        "name": "Doom Guard",
        "level": 8,
        "hp": 1350,
        "mana": 500
    },
    "ndrd": {
        "name": "Draenei Darkslayer",
        "level": 5,
        "hp": 525,
        "mana": 300
    },
    "ndrm": {
        "name": "Draenei Disciple",
        "level": 2,
        "hp": 280,
        "mana": 200
    },
    "ndrf": {
        "name": "Draenei Guardian",
        "level": 1,
        "hp": 240
    },
    "ndrh": {
        "name": "Draenei Harbinger",
        "level": 4,
        "hp": 450,
        "mana": 400
    },
    "ndrp": {
        "name": "Draenei Protector",
        "level": 2,
        "hp": 325
    },
    "ndrs": {
        "name": "Draenei Seer",
        "level": 6,
        "hp": 775,
        "mana": 500
    },
    "ndrw": {
        "name": "Draenei Watcher",
        "level": 3,
        "hp": 400
    },
    "nws1": {
        "name": "Dragon Hawk",
        "level": 5,
        "hp": 700
    },
    "ntrd": {
        "name": "Dragon Turtle",
        "level": 10,
        "hp": 2000,
        "mana": 600
    },
    "nehy": {
        "name": "Elder Hydra",
        "level": 7,
        "hp": 850,
        "mana": 400
    },
    "njga": {
        "name": "Elder Jungle Stalker",
        "level": 6,
        "hp": 900
    },
    "nsqe": {
        "name": "Elder Sasquatch",
        "level": 6,
        "hp": 950,
        "mana": 400
    },
    "nvde": {
        "name": "Elder Voidwalker",
        "level": 9,
        "hp": 1500,
        "mana": 500
    },
    "nwnr": {
        "name": "Elder Wendigo",
        "level": 6,
        "hp": 950
    },
    "nenf": {
        "name": "Enforcer",
        "level": 5,
        "hp": 500
    },
    "nele": {
        "name": "Enraged Elemental",
        "level": 4,
        "hp": 550
    },
    "nowe": {
        "name": "Enraged Wildkin",
        "level": 6,
        "hp": 950
    },
    "njgb": {
        "name": "Enranged Jungle Stalker",
        "level": 9,
        "hp": 1600,
        "mana": 600
    },
    "nerd": {
        "name": "Eredar Diabolist",
        "level": 6,
        "hp": 630,
        "mana": 300
    },
    "ners": {
        "name": "Eredar Sorceror",
        "level": 4,
        "hp": 425,
        "mana": 200
    },
    "nerw": {
        "name": "Eredar Warlock",
        "level": 9,
        "hp": 1350,
        "mana": 500
    },
    "nfod": {
        "name": "Faceless One Deathbringer",
        "level": 10,
        "hp": 1900,
        "mana": 500
    },
    "nfot": {
        "name": "Faceless One Terror",
        "level": 8,
        "hp": 1150,
        "mana": 400
    },
    "nfor": {
        "name": "Faceless One Trickster",
        "level": 6,
        "hp": 675,
        "mana": 300
    },
    "nhfp": {
        "name": "Fallen Priest",
        "level": 1,
        "hp": 240
    },
    "npfl": {
        "name": "Fel Beast",
        "level": 3,
        "hp": 390
    },
    "npfm": {
        "name": "Fel Ravager",
        "level": 7,
        "hp": 950,
        "mana": 300
    },
    "nfel": {
        "name": "Fel Stalker",
        "level": 5,
        "hp": 750,
        "mana": 200
    },
    "nfgu": {
        "name": "Felguard",
        "level": 2,
        "hp": 300
    },
    "nrvf": {
        "name": "Fire Revenant",
        "level": 3,
        "traits": "Undead",
        "hp": 340,
        "mana": 300
    },
    "nftb": {
        "name": "Forest Troll Berserker",
        "level": 4,
        "hp": 450
    },
    "nfsh": {
        "name": "Forest Troll High Priest",
        "level": 4,
        "hp": 450,
        "mana": 300
    },
    "nfsp": {
        "name": "Forest Troll Shadow Priest",
        "level": 2,
        "hp": 240,
        "mana": 200
    },
    "nftk": {
        "name": "Forest Troll Warlord",
        "level": 6,
        "hp": 750
    },
    "nftr": {
        "name": "Forest Troll",
        "level": 2,
        "hp": 300
    },
    "nftt": {
        "name": "Forest Troll Trapper",
        "level": 3,
        "hp": 400
    },
    "nfgo": {
        "name": "Forgotten One",
        "level": 15,
        "hp": 4000,
        "mana": 1000
    },
    "nfgt": {
        "name": "Forgotten One Tentacle",
        "level": 1,
        "traits": "Ward",
        "hp": 200
    },
    "nrvs": {
        "name": "Frost Revenant",
        "level": 4,
        "traits": "Undead",
        "hp": 450,
        "mana": 300
    },
    "nfrl": {
        "name": "Furbolg",
        "level": 4,
        "hp": 550
    },
    "nfrg": {
        "name": "Furbolg Champion",
        "level": 7,
        "hp": 950
    },
    "nfre": {
        "name": "Furbolg Elder Shaman",
        "level": 7,
        "hp": 950,
        "mana": 500
    },
    "nfrp": {
        "name": "Pandaren",
        "level": 4,
        "hp": 550
    },
    "nfrs": {
        "name": "Furbolg Shaman",
        "level": 4,
        "hp": 550,
        "mana": 300
    },
    "nfrb": {
        "name": "Furbolg Tracker",
        "level": 6,
        "hp": 950,
        "mana": 400
    },
    "nfra": {
        "name": "Furbolg Ursa Warrior",
        "level": 8,
        "hp": 1100,
        "mana": 500
    },
    "ntrg": {
        "name": "Gargantuan Sea Turtle",
        "level": 7,
        "hp": 1250
    },
    "ngh1": {
        "name": "Ghost",
        "level": 3,
        "traits": "Undead",
        "hp": 300,
        "mana": 300
    },
    "nplg": {
        "name": "Giant Polar Bear",
        "level": 6,
        "hp": 900
    },
    "ntrt": {
        "name": "Giant Sea Turtle",
        "level": 4,
        "hp": 375
    },
    "nskg": {
        "name": "Giant Skeleton Warrior",
        "level": 3,
        "traits": "Undead",
        "hp": 380
    },
    "nsgt": {
        "name": "Giant Spider",
        "level": 4,
        "hp": 550
    },
    "nwwg": {
        "name": "Giant Frost Wolf",
        "level": 4,
        "hp": 550
    },
    "nwlg": {
        "name": "Giant Wolf",
        "level": 4,
        "hp": 550
    },
    "ngns": {
        "name": "Gnoll Assassin",
        "level": 3,
        "hp": 320
    },
    "ngnb": {
        "name": "Gnoll Brute",
        "level": 3,
        "hp": 400
    },
    "ngnv": {
        "name": "Gnoll Overseer",
        "level": 5,
        "hp": 750
    },
    "ngna": {
        "name": "Gnoll Poacher",
        "level": 1,
        "hp": 240
    },
    "ngno": {
        "name": "Gnoll",
        "level": 1,
        "hp": 240
    },
    "ngnw": {
        "name": "Gnoll Warden",
        "level": 3,
        "hp": 330,
        "mana": 300
    },
    "nggr": {
        "name": "Granite Golem",
        "level": 9,
        "hp": 1500,
        "mana": 600
    },
    "nvdg": {
        "name": "Greater Voidwalker",
        "level": 6,
        "hp": 750,
        "mana": 400
    },
    "ngrd": {
        "name": "Green Dragon",
        "level": 10,
        "hp": 2200
    },
    "ngrw": {
        "name": "Green Dragon Whelp",
        "level": 3,
        "hp": 340
    },
    "ngdk": {
        "name": "Green Drake",
        "level": 6,
        "hp": 950
    },
    "nspg": {
        "name": "Forest Spider",
        "level": 1,
        "hp": 240
    },
    "nhrh": {
        "name": "Harpy Storm-hag",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "nhrq": {
        "name": "Harpy Queen",
        "level": 7,
        "hp": 750,
        "mana": 400
    },
    "nhrr": {
        "name": "Harpy Rogue",
        "level": 3,
        "hp": 340
    },
    "nhar": {
        "name": "Harpy Scout",
        "level": 1,
        "hp": 210
    },
    "nhrw": {
        "name": "Harpy Windwitch",
        "level": 3,
        "hp": 280,
        "mana": 300
    },
    "nwe1": {
        "name": "Hawk",
        "level": 2,
        "hp": 300
    },
    "nhhr": {
        "name": "Heretic",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "nhyd": {
        "name": "Hydra",
        "level": 6,
        "hp": 575
    },
    "nhyh": {
        "name": "Hydra Hatchling",
        "level": 3,
        "hp": 350
    },
    "nhym": {
        "name": "Hydromancer",
        "level": 2,
        "hp": 405,
        "mana": 400
    },
    "nrvi": {
        "name": "Ice Revenant",
        "level": 8,
        "traits": "Undead",
        "hp": 1100,
        "mana": 500
    },
    "nits": {
        "name": "Ice Troll Berserker",
        "level": 4,
        "hp": 450
    },
    "nith": {
        "name": "Ice Troll High Priest",
        "level": 4,
        "hp": 450,
        "mana": 300
    },
    "nitp": {
        "name": "Ice Troll Priest",
        "level": 2,
        "hp": 240,
        "mana": 200
    },
    "nitt": {
        "name": "Ice Troll Trapper",
        "level": 3,
        "hp": 400
    },
    "nitw": {
        "name": "Ice Troll Warlord",
        "level": 6,
        "hp": 750
    },
    "nitr": {
        "name": "Ice Troll",
        "level": 2,
        "hp": 300
    },
    "nmit": {
        "name": "Icetusk Mammoth",
        "level": 5,
        "hp": 925
    },
    "ninf": {
        "name": "Infernal",
        "level": 8,
        "hp": 1500,
        "mana": "-"
    },
    "nina": {
        "name": "Infernal Automaton",
        "level": 10,
        "traits": "Mechanical",
        "hp": 1500,
        "mana": 400
    },
    "ninc": {
        "name": "Infernal Contraption",
        "level": 5,
        "traits": "Mechanical",
        "hp": 600
    },
    "ninm": {
        "name": "Infernal Machine",
        "level": 8,
        "traits": "Mechanical",
        "hp": 1200,
        "mana": 350
    },
    "njg1": {
        "name": "Jungle Stalker",
        "level": 3,
        "hp": 400
    },
    "nkob": {
        "name": "Kobold",
        "level": 1,
        "hp": 240
    },
    "nkog": {
        "name": "Kobold Geomancer",
        "level": 3,
        "hp": 300,
        "mana": 300
    },
    "nkol": {
        "name": "Kobold Taskmaster",
        "level": 5,
        "hp": 650
    },
    "nkot": {
        "name": "Kobold Tunneler",
        "level": 3,
        "hp": 325
    },
    "nvdl": {
        "name": "Lesser Voidwalker",
        "level": 1,
        "hp": 240
    },
    "nltl": {
        "name": "Lightning Lizard",
        "level": 2,
        "hp": 280,
        "mana": 200
    },
    "nrvl": {
        "name": "Lightning Revenant",
        "level": 6,
        "traits": "Undead",
        "hp": 750,
        "mana": 400
    },
    "nmgd": {
        "name": "Magnataur Destroyer",
        "level": 10,
        "hp": 2100,
        "mana": 500
    },
    "nmgr": {
        "name": "Magnataur Reaver",
        "level": 8,
        "hp": 1500,
        "mana": 350
    },
    "nmgw": {
        "name": "Magnataur Warrior",
        "level": 5,
        "hp": 900
    },
    "ndqp": {
        "name": "Maiden of Pain",
        "level": 8,
        "hp": 1050,
        "mana": 400
    },
    "nlds": {
        "name": "Makrura Deepseer",
        "level": 5,
        "hp": 480,
        "mana": 300
    },
    "nlpd": {
        "name": "Makrura Pooldweller",
        "level": 2,
        "hp": 210
    },
    "nlpr": {
        "name": "Makrura Prawn",
        "level": 1,
        "hp": 170
    },
    "nlps": {
        "name": "Makrura Prawn",
        "level": 1,
        "hp": 170
    },
    "nlsn": {
        "name": "Makrura Snapper",
        "level": 5,
        "hp": 620
    },
    "nlkl": {
        "name": "Makrura Tidal Lord",
        "level": 7,
        "hp": 800
    },
    "nltc": {
        "name": "Makrura Tidecaller",
        "level": 2,
        "hp": 240,
        "mana": 300
    },
    "nmam": {
        "name": "Mammoth",
        "level": 3,
        "hp": 450
    },
    "ngrk": {
        "name": "Mud Golem",
        "level": 2,
        "hp": 240,
        "mana": 300
    },
    "nmbg": {
        "name": "Mur'gul Blood-Gill",
        "level": 2,
        "hp": 300,
        "mana": 200
    },
    "nmcf": {
        "name": "Mur'gul Cliffrunner",
        "level": 1,
        "hp": 240
    },
    "nmrv": {
        "name": "Mur'gul Maurader",
        "level": 6,
        "hp": 1000
    },
    "nmsc": {
        "name": "Mur'gul Shadowcaster",
        "level": 7,
        "hp": 1000,
        "mana": 400
    },
    "nmsn": {
        "name": "Mur'gul Snarecaster",
        "level": 4,
        "hp": 375,
        "mana": 300
    },
    "nmtw": {
        "name": "Mur'gul Tidewarrior",
        "level": 3,
        "hp": 400
    },
    "nmfs": {
        "name": "Murloc Flesheater",
        "level": 3,
        "hp": 400
    },
    "nmrr": {
        "name": "Murloc Huntsman",
        "level": 2,
        "hp": 300
    },
    "nmmu": {
        "name": "Murloc Mutant",
        "level": 6,
        "hp": 750,
        "mana": 400
    },
    "nmrm": {
        "name": "Murloc Nightcrawler",
        "level": 3,
        "hp": 400
    },
    "nmpg": {
        "name": "Murloc Plaguebearer",
        "level": 2,
        "hp": 180
    },
    "nmrl": {
        "name": "Murloc Tiderunner",
        "level": 1,
        "hp": 240
    },
    "nnwq": {
        "name": "Nerubian Queen",
        "level": 7,
        "hp": 950,
        "mana": 500
    },
    "nnwr": {
        "name": "Nerubian Seer",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "nnws": {
        "name": "Nerubian Spider Lord",
        "level": 5,
        "hp": 750
    },
    "nnwa": {
        "name": "Nerubian Warrior",
        "level": 3,
        "hp": 400
    },
    "nnwl": {
        "name": "Nerubian Webspinner",
        "level": 3,
        "hp": 350,
        "mana": 300
    },
    "nndr": {
        "name": "Nether Dragon",
        "level": 10,
        "hp": 2200,
        "mana": 500
    },
    "nnht": {
        "name": "Nether Dragon Hatchling",
        "level": 3,
        "hp": 340
    },
    "nndk": {
        "name": "Nether Drake",
        "level": 6,
        "hp": 950
    },
    "nogl": {
        "name": "Ogre Lord",
        "level": 7,
        "hp": 950,
        "mana": 500
    },
    "nomg": {
        "name": "Ogre Magi",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "nogm": {
        "name": "Ogre Mauler",
        "level": 5,
        "hp": 850
    },
    "nogr": {
        "name": "Ogre Warrior",
        "level": 3,
        "hp": 400
    },
    "nfov": {
        "name": "Overlord",
        "level": 6,
        "hp": 775,
        "mana": 300
    },
    "nepl": {
        "name": "Plague Treant",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "nenp": {
        "name": "Poison Treant",
        "level": 3,
        "hp": 290,
        "mana": 300
    },
    "nplb": {
        "name": "Polar Bear",
        "level": 4,
        "hp": 475
    },
    "nfpl": {
        "name": "Polar Furbolg",
        "level": 4,
        "hp": 550
    },
    "nfpc": {
        "name": "Polar Furbolg Champion",
        "level": 7,
        "hp": 950
    },
    "nfpe": {
        "name": "Polar Furbolg Elder Shaman",
        "level": 8,
        "hp": 950,
        "mana": 500
    },
    "nfps": {
        "name": "Polar Furbolg Shaman",
        "level": 4,
        "hp": 550,
        "mana": 300
    },
    "nfpt": {
        "name": "Polar Furbolg Tracker",
        "level": 6,
        "hp": 950,
        "mana": 400
    },
    "nfpu": {
        "name": "Polar Furbolg Ursa Warrior",
        "level": 8,
        "hp": 1100,
        "mana": 500
    },
    "ndqs": {
        "name": "Queen Of Suffering",
        "level": 10,
        "hp": 1600,
        "mana": 500
    },
    "nrzt": {
        "name": "Quillboar",
        "level": 1,
        "hp": 240
    },
    "nqbh": {
        "name": "Quillboar Hunter",
        "level": 3,
        "hp": 375
    },
    "nrzb": {
        "name": "Razormane Brute",
        "level": 3,
        "hp": 400
    },
    "nrzg": {
        "name": "Razormane Chieftain",
        "level": 7,
        "hp": 950,
        "mana": 500
    },
    "nrzm": {
        "name": "Razormane Medicine Man",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "nrzs": {
        "name": "Razormane Scout",
        "level": 1,
        "hp": 240
    },
    "nrwm": {
        "name": "Red Dragon",
        "level": 10,
        "hp": 2200
    },
    "nrdk": {
        "name": "Red Dragon Whelp",
        "level": 3,
        "hp": 400
    },
    "nrdr": {
        "name": "Red Drake",
        "level": 6,
        "hp": 950
    },
    "nrel": {
        "name": "Reef Elemental",
        "level": 2,
        "hp": 300
    },
    "nwzg": {
        "name": "Renegade Wizard",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "ndrv": {
        "name": "Revenant of the Depths",
        "level": 8,
        "traits": "Undead",
        "hp": 1000,
        "mana": 500
    },
    "nsrv": {
        "name": "Revenant of the Seas",
        "level": 5,
        "traits": "Undead",
        "hp": 900
    },
    "ntrv": {
        "name": "Revenant of the Tides",
        "level": 3,
        "traits": "Undead",
        "hp": 375
    },
    "ngst": {
        "name": "Rock Golem",
        "level": 6,
        "hp": 675,
        "mana": 400
    },
    "nrog": {
        "name": "Rogue",
        "level": 3,
        "hp": 400
    },
    "nwzr": {
        "name": "Rogue Wizard",
        "level": 3,
        "hp": 340,
        "mana": 300
    },
    "nslr": {
        "name": "Salamander",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "nslh": {
        "name": "Salamander Hatchling",
        "level": 3,
        "hp": 400
    },
    "nsll": {
        "name": "Salamander Lord",
        "level": 10,
        "hp": 1800,
        "mana": 700
    },
    "nslv": {
        "name": "Salamander Vizier",
        "level": 7,
        "hp": 950,
        "mana": 500
    },
    "nsqt": {
        "name": "Sasquatch",
        "level": 5,
        "hp": 750
    },
    "nsqo": {
        "name": "Sasquatch Oracle",
        "level": 7,
        "hp": 950,
        "mana": 500
    },
    "nsty": {
        "name": "Satyr",
        "level": 1,
        "hp": 240
    },
    "nsth": {
        "name": "Satyr Hellcaller",
        "level": 9,
        "hp": 1100,
        "mana": 500
    },
    "nsts": {
        "name": "Satyr Shadowdancer",
        "level": 3,
        "hp": 340,
        "mana": 300
    },
    "nstl": {
        "name": "Satyr Soulstealer",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "nsat": {
        "name": "Satyr Trickster",
        "level": 1,
        "hp": 240,
        "mana": 200
    },
    "nsel": {
        "name": "Sea Elemental",
        "level": 5,
        "hp": 550
    },
    "nsgn": {
        "name": "Sea Giant",
        "level": 3,
        "hp": 350
    },
    "nsgb": {
        "name": "Sea Giant Behemoth",
        "level": 8,
        "hp": 1000,
        "mana": 400
    },
    "nsgh": {
        "name": "Sea Giant Hunter",
        "level": 5,
        "hp": 725
    },
    "ntrs": {
        "name": "Sea Turtle",
        "level": 2,
        "hp": 250
    },
    "ntrh": {
        "name": "Sea Turtle Hatchling",
        "level": 1,
        "hp": 220
    },
    "nsgg": {
        "name": "Siege Golem",
        "level": 9,
        "hp": 1900
    },
    "nska": {
        "name": "Skeleton Archer",
        "level": 1,
        "traits": "Undead",
        "hp": 180
    },
    "nskm": {
        "name": "Skeletal Marksman",
        "level": 3,
        "traits": "Undead",
        "hp": 300,
        "mana": 300
    },
    "nsko": {
        "name": "Skeletal Orc",
        "level": 3,
        "traits": "Undead",
        "hp": 375
    },
    "nsoc": {
        "name": "Skeletal Orc Champion",
        "level": 8,
        "traits": "Undead",
        "hp": 1100,
        "mana": 400
    },
    "nsog": {
        "name": "Skeletal Orc Grunt",
        "level": 5,
        "traits": "Undead",
        "hp": 850
    },
    "nske": {
        "name": "Skeletonwarrior",
        "level": 1,
        "traits": "Undead",
        "hp": 180
    },
    "nslf": {
        "name": "Sludge Flinger",
        "level": 3,
        "hp": 340,
        "mana": 300
    },
    "nslm": {
        "name": "Sludge Minion",
        "level": 1,
        "hp": 240,
        "mana": 200
    },
    "nsln": {
        "name": "Sludge Monstrosity",
        "level": 5,
        "hp": 600,
        "mana": 400
    },
    "nspr": {
        "name": "Spider",
        "level": 1,
        "hp": 240
    },
    "nscb": {
        "name": "Spider Crab Shorecrawler",
        "level": 1,
        "hp": 240
    },
    "nsc2": {
        "name": "Spider Crab Limbripper",
        "level": 3,
        "hp": 400
    },
    "nsc3": {
        "name": "Spider Crab Behemoth",
        "level": 5,
        "hp": 850
    },
    "nspd": {
        "name": "Spiderling",
        "level": 1,
        "hp": 240
    },
    "nspp": {
        "name": "Spirit Pig",
        "level": 2,
        "hp": 200
    },
    "nssp": {
        "name": "Spitting Spider",
        "level": 3,
        "hp": 400
    },
    "nogn": {
        "name": "Stonemaul Magi",
        "level": 7,
        "hp": 1060,
        "mana": 400
    },
    "nogo": {
        "name": "Stonemaul Ogre",
        "level": 6,
        "hp": 1060
    },
    "noga": {
        "name": "Stonemaul Warchief",
        "level": 11,
        "hp": 3300
    },
    "nstw": {
        "name": "Storm Wyrm",
        "level": 9,
        "hp": 1500,
        "mana": 600
    },
    "nsra": {
        "name": "Stormreaver Apprentice",
        "level": 1,
        "hp": 240
    },
    "nsrh": {
        "name": "Stormreaver Hermit",
        "level": 3,
        "hp": 340,
        "mana": 200
    },
    "nsrn": {
        "name": "Stormreaver Necrolyte",
        "level": 6,
        "hp": 675,
        "mana": 350
    },
    "nsrw": {
        "name": "Stormreaver Warlock",
        "level": 9,
        "hp": 1500,
        "mana": 500
    },
    "ndqn": {
        "name": "Succubus",
        "level": 3,
        "hp": 400
    },
    "nthl": {
        "name": "Thunder Lizard",
        "level": 6,
        "hp": 750,
        "mana": 400
    },
    "nwlt": {
        "name": "Timber Wolf",
        "level": 2,
        "hp": 300
    },
    "ntkc": {
        "name": "Tuskarr Chieftain",
        "level": 7,
        "hp": 950,
        "mana": "-"
    },
    "ntkf": {
        "name": "Tuskarr Fighter",
        "level": 2,
        "hp": 250
    },
    "ntkh": {
        "name": "Tuskarr Healer",
        "level": 3,
        "hp": 300,
        "mana": 200
    },
    "ntks": {
        "name": "Tuskarr Sorceror",
        "level": 5,
        "hp": 475,
        "mana": 300
    },
    "ntka": {
        "name": "Tuskarr Spearman",
        "level": 2,
        "hp": 300
    },
    "ntkt": {
        "name": "Tuskarr Trapper",
        "level": 4,
        "hp": 475
    },
    "ntkw": {
        "name": "Tuskarr Warrior",
        "level": 4,
        "hp": 475
    },
    "nubk": {
        "name": "Unbroken Darkhunter",
        "level": 2,
        "hp": 250
    },
    "nubw": {
        "name": "Unbroken Darkweaver",
        "level": 5,
        "hp": 600,
        "mana": 200
    },
    "nubr": {
        "name": "Unbroken Rager",
        "level": 4,
        "hp": 475
    },
    "ndqt": {
        "name": "Vile Temptress",
        "level": 6,
        "hp": 750
    },
    "ndqv": {
        "name": "Vile Tormentor",
        "level": 5,
        "hp": 510,
        "mana": 200
    },
    "nvdw": {
        "name": "Voidwalker",
        "level": 3,
        "hp": 365,
        "mana": 200
    },
    "nwrg": {
        "name": "War Golem",
        "level": 6,
        "hp": 1000
    },
    "ncfs": {
        "name": "Watery Minion Cliffrunner",
        "level": 2,
        "hp": 240
    },
    "nsns": {
        "name": "Watery Minion Snarecaster",
        "level": 3,
        "hp": 375,
        "mana": 300
    },
    "ntws": {
        "name": "Watery Minion Tidewarrior",
        "level": 2,
        "hp": 400
    },
    "nwen": {
        "name": "Wendigo",
        "level": 4,
        "hp": 550
    },
    "nwns": {
        "name": "Wendigo Shaman",
        "level": 7,
        "hp": 950,
        "mana": 500
    },
    "nwwf": {
        "name": "Frost Wolf",
        "level": 2,
        "hp": 300
    },
    "nowb": {
        "name": "Wildkin",
        "level": 4,
        "hp": 550
    },
    "ngh2": {
        "name": "Wraith",
        "level": 6,
        "traits": "Undead",
        "hp": 750,
        "mana": 400
    },
    "nzom": {
        "name": "Zombie",
        "level": 1,
        "traits": "Undead",
        "hp": 240
    }
};


const itemCodes = {
    "clsd": { "name": "Cloak of Shadows", "type": "Permanent", "level": 1 },
    "rst1": { "name": "Gauntlets of Ogre Strength +3", "type": "Permanent", "level": 1 },
    "rin1": { "name": "Mantle of Intelligence +3", "type": "Permanent", "level": 1 },
    "rag1": { "name": "Slippers of Agility +3", "type": "Permanent", "level": 1 },
    "rat6": { "name": "Claws of Attack +6", "type": "Permanent", "level": 2 },
    "gcel": { "name": "Gloves of Haste", "type": "Permanent", "level": 2 },
    "rde1": { "name": "Ring of Protection +2", "type": "Permanent", "level": 2 },
    "rde2": { "name": "Ring of Protection +3", "type": "Permanent", "level": 2 },
    "cnob": { "name": "Circlet of Nobility", "type": "Permanent", "level": 2 },
    "rat9": { "name": "Claws of Attack +9", "type": "Permanent", "level": 3 },
    "crys": { "name": "Crystal Ball", "type": "Permanent", "level": 3 },
    "penr": { "name": "Pendant of Energy", "type": "Permanent", "level": 3 },
    "rlif": { "name": "Ring of Regeneration", "type": "Permanent", "level": 3 },
    "evtl": { "name": "Talisman of Evasion", "type": "Permanent", "level": 3 },
    "rde3": { "name": "Ring of Protection +4", "type": "Permanent", "level": 3 },
    "belv": { "name": "Boots of Quel'Thalas +6", "type": "Permanent", "level": 4 },
    "ciri": { "name": "Robe of the Magi +6", "type": "Permanent", "level": 4 },
    "bgst": { "name": "Belt of Giant Strength +6", "type": "Permanent", "level": 4 },
    "afac": { "name": "Alleria's Flute of Accuracy", "type": "Permanent", "level": 4 },
    "brac": { "name": "Runed Bracers", "type": "Permanent", "level": 4 },
    "sbch": { "name": "Scourge Bone Chimes", "type": "Permanent", "level": 4 },
    "rwiz": { "name": "Sobi Mask", "type": "Permanent", "level": 4 },
    "lhst": { "name": "The Lion Horn of Stormwind", "type": "Permanent", "level": 4 },
    "ajen": { "name": "Ancient Janggo of Endurance", "type": "Permanent", "level": 5 },
    "ratc": { "name": "Claws of Attack +12", "type": "Permanent", "level": 5 },
    "clfm": { "name": "Cloak of Flames", "type": "Permanent", "level": 5 },
    "hval": { "name": "Helm of Valor", "type": "Permanent", "level": 5 },
    "hcun": { "name": "Hood of Cunning", "type": "Permanent", "level": 5 },
    "kpin": { "name": "Khadgar's Pipe of Insight", "type": "Permanent", "level": 5 },
    "lgdh": { "name": "Legion Doom-Horn", "type": "Permanent", "level": 5 },
    "mcou": { "name": "Medallion of Courage", "type": "Permanent", "level": 5 },
    "ward": { "name": "Warsong Battle Drums", "type": "Permanent", "level": 5 },
    "spsh": { "name": "Amulet of Spell Shield", "type": "Permanent", "level": 6 },
    "rhth": { "name": "Khadgar's Gem of Health", "type": "Permanent", "level": 6 },
    "odef": { "name": "Orb of Darkness", "type": "Permanent", "level": 6 },
    "pmna": { "name": "Pendant of Mana", "type": "Permanent", "level": 6 },
    "rde4": { "name": "Ring of Protection +5", "type": "Permanent", "level": 6 },
    "ssil": { "name": "Staff of Silence", "type": "Permanent", "level": 6 },
    "ratf": { "name": "Claws of Attack +15", "type": "Artifact", "level": 7 },
    "desc": { "name": "Kelen's Dagger of Escape", "type": "Artifact", "level": 7 },
    "ofro": { "name": "Orb of Frost", "type": "Artifact", "level": 7 },
    "ckng": { "name": "Crown of Kings +5", "type": "Artifact", "level": 8 },
    "modt": { "name": "Mask of Death", "type": "Artifact", "level": 8 },
    "tkno": { "name": "Tome of Power", "type": "Artifact", "level": 8 },
    "rej3": { "name": "Replenishment Potion", "type": "Charged", "level": 2 },
    "wswd": { "name": "Sentry Wards", "type": "Charged", "level": 2 },
    "will": { "name": "Wand of Illusion", "type": "Charged", "level": 2 },
    "wlsd": { "name": "Wand of Lightning Shield", "type": "Charged", "level": 2 },
    "pghe": { "name": "Potion of Greater Healing", "type": "Charged", "level": 3 },
    "pgma": { "name": "Potion of Greater Mana", "type": "Charged", "level": 3 },
    "pnvu": { "name": "Potion of Invulnerability", "type": "Charged", "level": 3 },
    "sror": { "name": "Scroll of the Beast", "type": "Charged", "level": 3 },
    "woms": { "name": "Wand of Mana Stealing", "type": "Charged", "level": 3 },
    "ankh": { "name": "Ankh of Reincarnation", "type": "Charged", "level": 4 },
    "fgsk": { "name": "Book of the Dead", "type": "Charged", "level": 4 },
    "whwd": { "name": "Healing Wards", "type": "Charged", "level": 4 },
    "hlst": { "name": "Health Stone", "type": "Charged", "level": 4 },
    "mnst": { "name": "Mana Stone", "type": "Charged", "level": 4 },
    "wcyc": { "name": "Wand of the Wind", "type": "Charged", "level": 4 },
    "pdiv": { "name": "Potion of Divinity", "type": "Charged", "level": 5 },
    "pres": { "name": "Potion of Restoration", "type": "Charged", "level": 5 },
    "fgrd": { "name": "Red Drake Egg", "type": "Charged", "level": 5 },
    "sres": { "name": "Scroll of Restoration", "type": "Charged", "level": 5 },
    "fgfh": { "name": "Spiked Collar", "type": "Charged", "level": 5 },
    "fgrg": { "name": "Stone Token", "type": "Charged", "level": 5 },
    "totw": { "name": "Talisman of the Wild", "type": "Charged", "level": 5 },
    "wild": { "name": "Amulet of the Wild", "type": "Charged", "level": 6 },
    "fgdg": { "name": "Demonic Figurine", "type": "Charged", "level": 6 },
    "shar": { "name": "Ice Shard", "type": "Charged", "level": 6 },
    "infs": { "name": "Inferno Stone", "type": "Charged", "level": 6 },
    "sand": { "name": "Scroll of Animate Dead", "type": "Charged", "level": 6 },
    "srrc": { "name": "Scroll of Resurrection", "type": "Charged", "level": 6 },
    "rhe1": { "name": "Rune of Lesser Healing", "type": "Power Up", "level": 0 },
    "rhe2": { "name": "Rune of Healing", "type": "Power Up", "level": 0 },
    "rhe3": { "name": "Rune of Greater Healing", "type": "Power Up", "level": 0 },
    "rman": { "name": "Rune of Mana", "type": "Power Up", "level": 0 },
    "rre1": { "name": "Rune of Lesser Resurrection", "type": "Power Up", "level": 0 },
    "rre2": { "name": "Rune of Greater Resurrection", "type": "Power Up", "level": 0 },
    "rwat": { "name": "Rune of the Watcher", "type": "Power Up", "level": 0 },
    "rspd": { "name": "Rune of Speed", "type": "Power Up", "level": 0 },
    "manh": { "name": "Manual of Health", "type": "Power Up", "level": 1 },
    "tstr": { "name": "Tome of Strength", "type": "Power Up", "level": 1 },
    "tint": { "name": "Tome of Intelligence", "type": "Power Up", "level": 1 },
    "tdex": { "name": "Tome of Dexterity", "type": "Power Up", "level": 1 },
    "tpow": { "name": "Tome of Knowledge", "type": "Power Up", "level": 2 },
    "tst2": { "name": "Tome of Strength +2", "type": "Power Up", "level": 2 },
    "tin2": { "name": "Tome of Intelligence +2", "type": "Power Up", "level": 2 },
    "tdx2": { "name": "Tome of Dexterity +2", "type": "Power Up", "level": 2 },
    "fgbd": { "name": "Blue Drake Egg", "type": "Charged", "level": 5 },
    "iotw": { "name": "Idol of the Wild", "type": "Charged", "level": 5 },
    "ccmd": { "name": "Scepter of Mastery", "type": "Charged", "level": 6 },
    "scav": { "name": "Scepter of Avarice", "type": "Charged", "level": 6 },
    "engr": { "name": "Engraved Scale", "type": "Charged", "level": 6 }
};

const dropTableCodes = {
    "YiI1": {
        "type": "Permanent",
        "level": 1,
        "items": ["clsd", "rst1", "rin1", "rag1"]
    },
    "YiI2": {
        "type": "Permanent",
        "level": 2,
        "items": ["cnob", "rat6", "gcel", "rde2"]
    },
    "YiI3": {
        "type": "Permanent",
        "level": 3,
        "items": ["rat9", "crys", "penr", "rlif", "evtl", "rde3"]
    },
    "YiI4": {
        "type": "Permanent",
        "level": 4,
        "items": ["belv", "ciri", "bgst", "afac", "brac", "sbch", "rwiz", "lhst"]
    },
    "YiI5": {
        "type": "Permanent",
        "level": 5,
        "items": ["ajen", "ratc", "clfm", "hval", "hcun", "kpin", "lgdh", "mcou", "ward"]
    },
    "YiI6": {
        "type": "Permanent",
        "level": 6,
        "items": ["spsh", "rhth", "odef", "pmna", "rde4", "ssil"]
    },
    "YlI7": {
        "type": "Artifact",
        "level": 7,
        "items": ["ratf", "desc", "ofro", "infs"]
    },
    "YlI8": {
        "type": "Artifact",
        "level": 8,
        "items": ["ckng", "modt", "tkno"]
    },
    "YjI1": {
        "type": "Charged",
        "level": 1,
        "items": [] // it really is an empty item table
    },
    "YjI2": {
        "type": "Charged",
        "level": 2,
        "items": ["rej3", "wswd", "will", "wlsd"]
    },
    "YjI3": {
        "type": "Charged",
        "level": 3,
        "items": ["pghe", "pgma", "pnvu", "sror", "woms"]
    },
    "YjI4": {
        "type": "Charged",
        "level": 4,
        "items": ["ankh", "fgsk", "whwd", "hlst", "mnst", "wcyc"]
    },
    "YjI5": {
        "type": "Charged",
        "level": 5,
        "items": ["pdiv", "pres", "fgbd", "sres", "fgfh", "fgrg", "iotw"]
    },
    "YjI6": {
        "type": "Charged",
        "level": 6,
        "items": ["wild", "fgdg", "shar", "ccmd", "scav", "engr"]
    },
    "YkI1": {
        "type": "Power Up",
        "level": 1,
        "items": ["manh", "tstr", "tint", "tdex"]
    },
    "YkI2": {
        "type": "Power Up",
        "level": 2,
        "items": ["tpow", "tst2", "tin2", "tdx2"]
    },
    "YkI3": {
        "type": "Power Up",
        "level": 3,
        "items": [] // another empty table, mistakenly (?) used on (6)Timbermaw Hold
    }
}

const levelExp = {
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

if (typeof window === 'undefined') {
    module.exports.neutralBuildingCodes = neutralBuildingCodes;
    module.exports.creepCodes = creepCodes;
    module.exports.itemCodes = itemCodes;
    module.exports.dropTableCodes = dropTableCodes;
}