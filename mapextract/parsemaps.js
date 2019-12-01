const Translator = require('wc3maptranslator');
const glob = require("glob")
const fs = require('fs');
const { execSync } = require('child_process');

// Edit mapsDir to match your user folder
const mapsDir = 'C:\\Users\\sverr\\Documents\\Warcraft III Beta\\Maps\\Download';
const infoFile = 'war3map.w3i';
const mapInfoFile = 'mapinfo.json';

const extractInfo = mapPath => {
  // Edit MPQExtractor bin file if not on Windows
  execSync(`MPQExtractor.exe -e ${infoFile} -o . "${mapPath}"`);
  return infoFile;
}

const parseInfo = infoPath => {
  const data = fs.readFileSync(infoPath);
  var infoResult = new Translator.Info.warToJson(data).json;
  return {
    x: [infoResult.camera.bounds[0], infoResult.camera.bounds[2]],
    y: [infoResult.camera.bounds[1], infoResult.camera.bounds[3]],
    start: infoResult.players.map(p => [p.startingPos.x, p.startingPos.y])
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

  const infoFile = extractInfo(mapPath);
  try {
    const info = parseInfo(infoFile);
    return [name, info];
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
});
