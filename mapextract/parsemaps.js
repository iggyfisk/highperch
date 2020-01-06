const Translator = require('wc3maptranslator');
const glob = require("glob")
const fs = require('fs');
const { execSync } = require('child_process');

// Edit mapsDir to match your user folder
const mapsDir = 'C:\\Users\\sverr\\Documents\\Warcraft III Beta\\Maps\\Download';
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
    y: [infoResult.camera.bounds[1], infoResult.camera.bounds[3]],
    start: infoResult.players.map(p => [p.startingPos.x, p.startingPos.y])
  };
}

const parseUnits = editorVersion => {
  const data = fs.readFileSync(unitsFile);
  var unitsResult = new Translator.Units.warToJson(data, editorVersion).json;
  const goldMines = [];

  unitsResult.forEach(u => {
    switch (u.type) {
      case 'ngol':
        goldMines.push({ x: u.position[0], y: u.position[1], g: u.gold });
        break;
    }
  });

  return {
    mines: goldMines,
  };
}

const mapName = new RegExp('^.*\\/(\\(\\d*\\).*)\\.w3x$');
const parseMap = mapPath => {
  const nameMatch = mapPath.match(mapName);
  if (!nameMatch) {
    console.log('Ladder map name not found, skipping', mapPath);
    return null;
  }
  const name = nameMatch[1].toLowerCase();

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

glob(mapsDir + '/**/*.w3x', null, function (err, files) {
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
