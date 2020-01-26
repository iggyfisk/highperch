const Translator = require('wc3maptranslator');
const glob = require("glob")
const fs = require('fs');
const { execSync } = require('child_process');

// Edit mapsDir to match your user folder
const mapsDir = 'C:\\Users\\tkerr\\Documents\\Warcraft III Beta\\Maps\\to-parse';
const infoFile = 'war3map.w3i';
const unitsFile = 'war3mapunits.doo';
const mapInfoFile = 'mapinfo.json';

const extractFile = (fileName, mapPath) => {
  // Edit MPQExtractor bin file if not on Windows
  execSync(`MPQExtractor.exe -e ${fileName} -o . "${mapPath}"`);
}

const parseInfo = () => {
  const data = fs.readFileSync(infoFile);
  var infoResult = new Translator.Info.warToJson(data).json;
  return {
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

  unitsResult.forEach(u => {
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
    }
  });

  return {
    starts: startingLocations,
    mines: goldMines,
    neutral_buildings: neutralBuildings
  };
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
  try {
    const info = parseInfo();
    const units = parseUnits(info.editorVersion);

    delete info.editorVersion;
    return [name, { ...info, ...units }];
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
});
