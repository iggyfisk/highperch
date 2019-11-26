const W3GReplay = require('w3gjs');
const { ActionBlockList } = require('./node_modules/w3gjs/dist/lib/parsers/actions');
const { buildings } = require('./node_modules/w3gjs/dist/lib/mappings');
const { writeFileSync } = require('fs');

const inputPath = process.argv.length >= 3 ? process.argv[2] : null;
const outputPath = process.argv.length >= 4 ? process.argv[3] : null;
if (!inputPath || !outputPath) {
  console.error('Enter input w3g and output json paths');
  return 1;
}

const Parser = new W3GReplay();
const teams = [];
let teamsLeft = [];
const playerTeams = [];
const leaveEvents = [];
let winningTeamId = null;
let winningTeamConfirmed = false;

Parser.on('gamemetadata', (metaData) => {
  metaData.playerSlotRecords.forEach(player => {
    // Team 24 are observers
    if (player.teamId == 24) return;
    if (player.computerFlag) return;

    playerTeams[player.playerId] = player.teamId;
    if (!teams[player.teamId]) {
      teams[player.teamId] = [];
      teamsLeft.push(player.teamId);
    }
    teams[player.teamId][player.playerId] = true;
  });
});

let lastLeaveEventMs = 0;
Parser.on('gamedatablock', (block) => {
  switch (block.type) {
    case 23:
      const { playerId } = block;
      const ms = Parser.msElapsed;

      // Non-player left the game
      if (playerTeams[playerId] === undefined) break;

      const teamId = playerTeams[playerId];
      teams[teamId][playerId] = false;
      leaveEvents.push({ playerId, ms });

      if (!teams[teamId].some(p => !!p)) {
        teamsLeft = teamsLeft.filter(tId => tId !== teamId);
      }

      if (winningTeamId == null && teamsLeft.length === 1) {
        winningTeamId = teamsLeft[0];
        // Check for a likely crash where everyone leaves at the same time out of order
        winningTeamConfirmed = lastLeaveEventMs !== ms;
      }
      lastLeaveEventMs = ms;
      break;
  }
});

const pauseEvents = [];
const playerBuildings = {};
Parser.on('timeslotblock', (timeSlotBlock) => {
  timeSlotBlock.actions.forEach(actionBlock => {
    const { playerId, actions } = actionBlock;
    ActionBlockList.parse(actions).forEach(action => {
      switch (action.actionId) {
        case 1:
          pauseEvents.push({ playerId, ms: Parser.msElapsed, pause: true });
          break;
        case 2:
          pauseEvents.push({ playerId, ms: Parser.msElapsed, pause: false });
          break;
        case 0x11:
          const { itemId } = action;
          if (itemId.type !== 'alphanumeric' && buildings[itemId.value]) {
            if (!playerBuildings[playerId]) playerBuildings[playerId] = [];
            playerBuildings[playerId].push({ id: itemId.value, ms: Parser.msElapsed, x: action.targetX, y: action.targetY });
          }
          break;
        // I forgot about tavern resurrection. RIP
        /*
        case 18:
          // Use ability with target and object
          const { itemId :{ value } } = action;

          if (value[0] == 89 && value[1] == 0 && value[2] == 19 && value[3] == 0) {
            // Revive hero
            if (!heroRevives[playerId]) heroRevives[playerId] = [];
            const time = Parser.msElapsed;
            console.log('Herorevive', playerId, time);
          }
          break;          
        case 29:
          // Revive cancelled
          if (!heroRevives[playerId]) heroRevives[playerId] = [];
          const time = Parser.msElapsed;
          console.log('Hero revive cancelled', time);
          break;
        */
      }
    });
  });
});

// All callbacks set, start parsing!
const replay = Parser.parse(inputPath);

// Figure out who saved and who won by looking at leave order
const replaySaverPlayerId = leaveEvents.length
  ? leaveEvents[leaveEvents.length - 1].playerId
  : null;

if (!winningTeamConfirmed && replaySaverPlayerId) {
  // If there were only 2 teams left after the replay saver left, guess that the other team won
  const replaySaverTeamId = playerTeams[replaySaverPlayerId];
  teamsLeft = teamsLeft.filter(tId => tId !== replaySaverTeamId);
  if (teamsLeft.length == 1) {
    winningTeamId = teamsLeft[0];
  }
}
replay.saverPlayerId = replaySaverPlayerId;
replay.winningTeamId = winningTeamId;
replay.winningTeamConfirmed = winningTeamConfirmed;
replay.leaveEvents = leaveEvents;

// Clean double chats from replay saver, bug in Reforged beta, Blizzard may have fixed it since
const sanitizedChat = [];
let lastSaverChatMs = 0;
let lastSaverChatMessage = null;
replay.chat.forEach(c => {
  const { playerId, timeMS, message } = c;
  if (playerId == replaySaverPlayerId) {
    if ((timeMS - lastSaverChatMs) < 500 && message == lastSaverChatMessage) {
      return;
    }
    lastSaverChatMs = timeMS;
    lastSaverChatMessage = message;
  }

  // Fuck these inconsistent timestamp attribute names
  c.ms = c.timeMS;
  delete c.timeMS;

  // Looks pointless to me, easy to restore
  delete c.byteCount;
  delete c.type;
  delete c.flags;

  sanitizedChat.push(c);
});
replay.chat = sanitizedChat;

// Include pauses
replay.pauseEvents = pauseEvents;

// Add X and Y coordinates to building order
replay.players.forEach(p => {
  p['buildings']['order'].forEach((b, i) => {
    if (!playerBuildings[p['id']][i]) {
      throw "w3gjs and highparser mismatch"
    }
  });
  // Replace with our location-aware list
  p['buildings']['order'] = playerBuildings[p['id']];
});

writeFileSync(outputPath, JSON.stringify(replay));
return 0;