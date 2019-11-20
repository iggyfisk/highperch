const W3GReplay = require('w3gjs');
const { writeFileSync } = require('fs');

const inputPath = process.argv.length >= 3 ? process.argv[2] : null;
const outputPath = process.argv.length >= 4 ? process.argv[3] : null;
if (!inputPath || !outputPath) {
  console.error('Enter input w3g and output json paths');
  return 1;
}

const Parser = new W3GReplay();
const replay = Parser.parse(inputPath);
writeFileSync(outputPath, JSON.stringify(replay));
return 0;
