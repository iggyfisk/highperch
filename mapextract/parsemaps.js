const Translator = require('wc3maptranslator');
const glob = require("glob")
const fs = require('fs');
const { execSync } = require('child_process');
const mapCodes = require('../perchweb/static/script/maplib.js')

// Edit mapsDir to match your user folder
// const mapsDir = 'C:\\Users\\tkerr\\Documents\\Warcraft III Beta\\Maps\\to-parse';
const mapsDir = '/Users/tkerr/Downloads/to-parse';
const infoFile = 'war3map.w3i';
const unitsFile = 'war3mapunits.doo';
const stringsFile = 'war3map.wts';
const mapInfoFile = 'mapinfo.json';

const extractFile = (fileName, mapPath) => {
  // Edit MPQExtractor bin file if not on Windows
  // execSync(`MPQExtractor.exe -e ${fileName} -o . "${mapPath}"`);
  execSync(`./MPQExtractor -e ${fileName} -o . "${mapPath}"`);
}

const parseInfo = () => {
  const data = fs.readFileSync(infoFile);
  var infoResult = new Translator.Info.warToJson(data).json;
  return {
    titleStringIndex: parseInt(infoResult.map.name.match(/_(\d+)$/)[1]),
    editorVersion: infoResult.editorVersion,
    x: [infoResult.camera.bounds[0], infoResult.camera.bounds[2]],
    y: [infoResult.camera.bounds[1], infoResult.camera.bounds[3]]
  };
}

const parseUnits = editorVersion => {
  const data = fs.readFileSync(unitsFile);
  var unitsResult = new Translator.Units.warToJson(data, editorVersion).json;
  // https://gist.github.com/tylerkerr/de9464dd81988a8fed4c894f2b79f2b1
  const startingLocations = [];
  const goldMines = [];
  const neutralBuildings = [];
  const creeps = [];
  const critters = [];

  unitsResult.forEach(u => {
    const drops = [];
    if (u.droppable.length > 0) {
      u.droppable.forEach(drop => {
        if (mapCodes.dropTableCodes[drop[0]]) {
          drops.push(mapCodes.dropTableCodes[drop[0]]['items']);
        }
        else {
          drops.push(drop[0]);
        }
      });
    }
    switch (u.type) {
      case 'sloc':  // starting location
        {
          startingLocations.push({ x: u.position[0], y: u.position[1], player: u.player });
          break;
        }
      case 'ngol':  // goldmine
        {
          goldMines.push({ id: u.type, x: u.position[0], y: u.position[1], g: u.gold });
          break;
        }
      case 'ntav':  // tavern
        {
          neutralBuildings.push({ id: u.type, x: u.position[0], y: u.position[1], });
          break;
        }
      case 'ngme':  // goblin merchant, aka shop
        {
          neutralBuildings.push({ id: u.type, x: u.position[0], y: u.position[1] });
          break;
        }
      case 'ngad':  // goblin laboratory
        {
          neutralBuildings.push({ id: u.type, x: u.position[0], y: u.position[1] });
          break;
        }
      case 'nmer':  // merc camp: lordaeron summer
      case 'nmr0':  // village, village fall
      case 'nmr2':  // lordaeron fall
      case 'nmr3':  // lordaeron winter
      case 'nmr4':  // barrens
      case 'nmr5':  // ashenvale
      case 'nmr6':  // felwood
      case 'nmr7':  // northrend
      case 'nmr8':  // cityscape
      case 'nmr9':  // dalaran, dalaran ruins
      case 'nmra':  // dungeon
      case 'nmrb':  // underground
      case 'nmrc':  // sunken ruins
      case 'nmrd':  // icecrown glacier
      case 'nmre':  // outland
      case 'nmrf':  // black citadel
        {
          neutralBuildings.push({ id: u.type, x: u.position[0], y: u.position[1] });
          break;
        }
      case 'ndrk':  // dragon roost: black
      case 'ndru':  // blue
      case 'ndrz':  // bronze
      case 'ndrg':  // green
      case 'ndro':  // nether
      case 'ndrr':  // red
        {
          neutralBuildings.push({ id: u.type, x: u.position[0], y: u.position[1] });
          break;
        }
      case 'nmrk':  // marketplace
        {
          neutralBuildings.push({ id: u.type, x: u.position[0], y: u.position[1] });
          break;
        }
      case 'nfoh':  // fountain of health
      case 'nmoo':  // fountain of mana
      case 'bDNR':  // bDNR is the code for any random building! so this could break if there's ever a non-fountain random building in a map we care about
        {
          neutralBuildings.push({ id: u.type, x: u.position[0], y: u.position[1] });
          break;
        }
      case 'nwgt':  // way gate
      {
        neutralBuildings.push({ id: u.type, x: u.position[0], y: u.position[1] });
        break;
      }
      case 'nshp':  // Goblin Shipyard on (4)Islands.w3x. Todo: assets etc.
      {
        neutralBuildings.push({ id: u.type, x: u.position[0], y: u.position[1] });
        break;
      }
      case 'nshe':  // sheep
      case 'necr':  // rabbit
      case 'nfro':  // frog
      case 'npig':  // pig
      case 'ndog':  // dog
      case 'ndwm':  // dune worm
      case 'nfbr':  // fel boar
      case 'nrat':  // rat
      case 'nsno':  // snowy owl
      case 'nvul':  // vulture
      case 'npng':  // penguin
      case 'npnw':  // penguin (water)
      case 'ncrb':  // crab
      case 'nalb':  // albatross
      case 'nrac':  // raccoon
      case 'nder':  // stag
      case 'nhmc':  // hermit crab
      case 'nech':  // chicken
      case 'nshf':  // flying sheep
      case 'nskk':  // skink
      case 'nsea':  // seal
      case 'ebsh':  // night elf battleship
      case 'etrs':  // night elf transport ship
      case 'nvil':  // villager male
      case 'nvl2':  // villager male 2
      case 'nvlw':  // villager woman
      case 'zzrg':  // zergling
      case 'hrdh':  // pack horse
      case 'nsha':  // amphibious sheep
        {
          critters.push({ id: u.type, x: Math.round(u.position[0]), y: Math.round(u.position[1]) })
          break;
        }
      // nonfunctional neutral buildings like tents, murloc huts, etc
      case 'ntn2':
      case 'nten':
      case 'ntt2':
      case 'ntnt':
      case 'ncnt':
      case 'nct2':
      case 'nct1':
      case 'nth1':
      case 'nth0':
      case 'nmh1':
      case 'nmh0':
      case 'nfr2':
      case 'nfr1':
      case 'ngnh':
      case 'ngt2':
      case 'ndh1':
      case 'ndh0':
      case 'nfh0':
      case 'nfh1':
      case 'nnzg':
      case 'nhns':
      case 'nmg0':
      case 'nmg1':
      case 'nbse':
      case 'haro':  // Arcane Observatory on (8)RockQuarry.w3x, looks to be nonfunctional
        {
          break;
        }
      default:
        {
          creeps.push({ id: u.type, x: Math.round(u.position[0]), y: Math.round(u.position[1]), drops: drops })
        }
    }
  });

  return {
    starts: startingLocations,
    mines: goldMines,
    neutral_buildings: neutralBuildings,
    creeps: creeps,
    critters: critters
  };
}

const parseStrings = () => {
  const data = fs.readFileSync(stringsFile);
  var stringResult = new Translator.Strings.warToJson(data).json;
  return {
    strings: stringResult
  };
}

const creepsToCamps = creeps => {
  const pythDistance = (x0, x1, y0, y1) => {
    return Math.sqrt(((x0 - x1) ** 2) + ((y0 - y1) ** 2));
  }

  const arrayMean = x => x.reduce((a, b) => a + b, 0) / x.length

  const maxCampId = camps => Math.max(...camps.map(value => value['id']))

  const createCamp = (campId, creep) => {
    let newCamp = {};
    newCamp['id'] = campId;
    newCamp['x'] = creep['x'];
    newCamp['y'] = creep['y'];
    newCamp['level'] = mapCodes.creepCodes[creep['id']]['level'];
    newCamp['creeps'] = [];
    newCamp['creeps'].push(creep);
    return newCamp;
  }

  const addCreepToCamp = (camp, creep) => {
    let allX = [creep['x']];
    let allY = [creep['y']];
    camp['creeps'].forEach(creep => {
      allX.push(creep['x']);
      allY.push(creep['y']);
    })
    camp['x'] = Math.round(arrayMean(allX));
    camp['y'] = Math.round(arrayMean(allY));
    camp['level'] += mapCodes.creepCodes[creep['id']]['level'];
    const creepDupeIdx = camp['creeps'].findIndex((c => c['id'] === creep['id'] && c['drops'].length === 0))
    if (creepDupeIdx !== -1) {
      camp['creeps'][creepDupeIdx]['count'] += 1;
    } else {
      camp['creeps'].push(creep);
    }
    return camp;
  }

  const findCloseCampId = (creepCamps, maxDistance, creep) => {
    let found = false;
    creepCamps.forEach(camp => {
      distance = pythDistance(creep['x'], camp['x'], creep['y'], camp['y'])
      if (distance <= maxDistance) {
        found = camp['id'];
      }
    })
    return found;
  }

  const getCampById = (creepCamps, id) => {
    return creepCamps.filter(camp => camp['id'] === id)[0];
  }

  const removeCampById = (creepCamps, id) => {
    return creepCamps.filter(camp => camp['id'] != id);
  }

  // this seems to work, but may need tuning for maps not in the launch rotation
  // 500 is too low, 1200 is too high
  const campMaxDistance = 700;

  let creepCamps = [];
  let totalCreeps = 0;

  creeps.forEach(creep => {
    totalCreeps += 1;
    creep['count'] = 1;
    if (creepCamps.length === 0) {
      creepCamps.push(createCamp(0, creep));
    }
    else {
      let closeCampId = findCloseCampId(creepCamps, campMaxDistance, creep);
      if (closeCampId !== false) {
        let closeCamp = getCampById(creepCamps, closeCampId);
        creepCamps = removeCampById(creepCamps, closeCampId);
        creepCamps.push(addCreepToCamp(closeCamp, creep));
      }
      else {
        creepCamps.push(createCamp(maxCampId(creepCamps) + 1, creep));
      }
    }
  });
  // console.log('[+]', totalCreeps, "creeps in", creepCamps.length, "camps");
  return creepCamps;
}

const mapName = new RegExp('^.*\\/(\\(\\d*\\).*)\\.w3x$');
const parseMap = mapPath => {
  const nameMatch = mapPath.match(mapName);
  if (!nameMatch) {
    console.log('Ladder map name not found, skipping', mapPath);
    return null;
  }
  const name = nameMatch[1];

  extractFile(infoFile, mapPath);
  extractFile(unitsFile, mapPath);
  extractFile(stringsFile, mapPath);

  // console.log('[-] parsing', name);


  try {
    const info = parseInfo();
    const units = parseUnits(info.editorVersion);
    const creepCamps = creepsToCamps(units.creeps);
    const strings = parseStrings();
    const mapTitle = strings.strings[info.titleStringIndex.toString()]
    const totalCreeps = units.creeps.length;
    delete info.editorVersion;
    delete info.titleStringIndex;
    delete units.creeps;
    return [name, {'mapTitle': mapTitle, 'totalCreeps': totalCreeps, ...info, ...units, 'creepCamps': creepCamps }];
  } catch {
    return null;
  }
}

let mapInfo = {};
if (fs.existsSync(mapInfoFile)) {
  mapInfo = JSON.parse(fs.readFileSync(mapInfoFile));
}

glob(mapsDir + '/*.w3x', null, function (err, files) {
  if (err) throw err;
  files.forEach(path => {
    const parsed = parseMap(path);
    if (parsed) mapInfo[parsed[0]] = parsed[1];
    if (!parsed) console.log('Map failed:', path);
  });
  fs.writeFileSync(mapInfoFile, JSON.stringify(mapInfo));

  if (fs.existsSync(infoFile)) {
    fs.unlinkSync(infoFile);
  }
  if (fs.existsSync(unitsFile)) {
    fs.unlinkSync(unitsFile);
  }
  if (fs.existsSync(stringsFile)) {
    fs.unlinkSync(stringsFile);
  }
});
