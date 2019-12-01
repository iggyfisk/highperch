### .w3x map info extractor
Finds every downloaded .w3x map, extracts war3map.w3i from the MPQ, then parses the map bounds and starting locations into a JSON format ready to be consumed by perchweb, for the drawmap feature. MPQExtractor binaries for Windows and macOS provided, https://github.com/Kanma/MPQExtractor if you want to compile your own.

* Unless you want to start from scratch, copy the existing `mapinfo.json` to this folder.
* Edit parsemaps.js as needed (marked with comments)
* `node parsemaps.js`
* Move the new `mapinfo.json` to `perchweb/resource`
