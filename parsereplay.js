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
const playerSlots = []
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

  playerSlots.push(metaData.player.playerId);
  metaData.playerList.forEach(player => {
    playerSlots.push(player.playerId);
  });
});

const leaveReasons = {
  '01000000': 'left',
  '0c000000': 'gameEnd',
};
Parser.on('gamedatablock', (block) => {
  switch (block.type) {
    case 23:
      const { playerId } = block;
      const ms = Parser.msElapsed;

      // Non-player left the game
      if (playerTeams[playerId] === undefined) break;

      reason = leaveReasons[block.reason] || 'unknown';
      leaveEvents.push({ playerId, ms, reason });
  }
});

const pauseEvents = [];
const playerBuildings = {};
const tradeEvents = [];
const playerShareEvents = {};
//const heroRevives = {};
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
        case 0x50:
          if (!playerShareEvents[playerId]) playerShareEvents[playerId] = [];
          playerShareEvents[playerId].push({
            playerId: playerSlots[action.slotNumber],
            flags: action.flags,
            ms: Parser.msElapsed,
          });
          break;
        case 0x51:
          const recipientPlayerId = playerSlots[action.slotNumber];
          const recipientTeam = playerTeams[recipientPlayerId];
          const senderTeam = playerTeams[playerId];

          // Todo: identify why in at least one replay there are invalid trades
          if (recipientPlayerId == undefined) {
            console.log("Invalid resource trade: undefined recipient");
            console.log(Parser.msElapsed, playerId + '=>' + recipientPlayerId, ':', action.gold, 'gold', action.lumber, 'lumber')
            break;
          }

          if (recipientTeam !== senderTeam) {
            console.log("Invalid resource trade: wrong recipient team");
            console.log(Parser.msElapsed, playerId + '=>' + recipientPlayerId, ':', action.gold, 'gold', action.lumber, 'lumber')
            break;
          }

          tradeEvents.push({
            playerId,
            recipientPlayerId,
            ms: Parser.msElapsed,
            gold: action.gold,
            lumber: action.lumber,
          });
          break;
        /*case 18:
          // Use ability with target and object
          const { itemId: { value } } = action;
          if (value[2] == 19 && value[3] == 0) {
            // Todo: value[0] for altar resing third slot
            if (value[1] == 0 && (value[0] == 89 || value[0] == 96 || false)) {
              console.log('Altar revive', playerId, Parser.msElapsed, action.objectId1, action.objectId2);
            } else if (value[1] ==1 && (value[0] == 568 || value[0] == 569 || value[0] == 576)) {
              console.log('Tavern revive', playerId, Parser.msElapsed, action.objectId1, action.objectId2);
            }
          }
          break;
        case 29:
          // Revive cancelled
          if (!heroRevives[playerId]) heroRevives[playerId] = [];
          const time = Parser.msElapsed;
          console.log('Hero revive cancelled', playerId, time);
          break;*/
      }
    });
  });
});

// All callbacks set, start parsing!
const replay = Parser.parse(inputPath);

// Figure out who saved and who won by looking at leave order
const leaveLength = leaveEvents.length;
let replaySaverPlayerId;
if (!leaveLength) {
  replaySaverPlayerId = null;
} else if (leaveLength === 1) {
  replaySaverPlayerId = leaveEvents[0].playerId;  // Only one leave event
} else if (leaveEvents[leaveLength - 1].ms !== leaveEvents[leaveLength - 2].ms) {
  replaySaverPlayerId = leaveEvents[leaveLength - 1].playerId;  // Latest leave event
} else {
  const selfQuit = leaveEvents.filter(l => l.reason == 'left');
  if (selfQuit.length === 0) {
    replaySaverPlayerId = -1;   // Edge case: nobody left the game. Server kicked everyone?
  } else {
    replaySaverPlayerId = selfQuit[selfQuit.length - 1].playerId; // Latest non-gameEnd event
  }
}

// Check to see if we have significant amounts of doublechats occurring from a player not currently identified as saver.
// This will stop doing anything if Blizzard fixes replay saver double chats
const doubleChatCounts = {};
replay.players.forEach(p => {
  doubleChatCounts[p['id']] = 0;
});
let lastChatMs = 0;
let lastChatMessage = null;
let lastChatPlayerId = 0;

replay.chat.forEach(c => {
  const { playerId, timeMS, message } = c;
    if ((timeMS - lastChatMs) < 500 && message == lastChatMessage && playerId == lastChatPlayerId && message.length >= 3) {
      doubleChatCounts[playerId] += 1
    }
    lastChatPlayerId = playerId;
    lastChatMs = timeMS;
    lastChatMessage = message;
});

const doubleChatScore = Object.keys(doubleChatCounts).sort(function(x,y){return doubleChatCounts[y]-doubleChatCounts[x]});

if (doubleChatCounts[doubleChatScore[0]] > 0 && doubleChatScore[0] != replaySaverPlayerId) {
  console.log("Potential incorrect saver ID (" + replaySaverPlayerId + ") detected based on doublechats");
  if (doubleChatCounts[doubleChatScore[1]] === 0) {   // There was only one doublechatter
    replaySaverPlayerId = parseInt(doubleChatScore[0])
    console.log("New saver ID is", replaySaverPlayerId, "via unambiguous doublechats")
  } else if (doubleChatCounts[doubleChatScore[1]] <= doubleChatCounts[doubleChatScore[0]] / 4) {  // There was a primary doublechatter
    replaySaverPlayerId = parseInt(doubleChatScore[0])
    console.log("New saver ID is", replaySaverPlayerId, "from potentially ambiguous doublechats")
  } else {
    console.log("Double chats found, but were inconclusive")
  }
}

// Try do determine game winner
saverLeft = false;
leaveEvents.forEach(l => {
  const teamId = playerTeams[l.playerId];
  teams[teamId][l.playerId] = false;

  if (!teams[teamId].some(p => !!p)) {
    // If only one team remains, they probably won. If the saver hasn't left at that point, 
    // they DEFINITELY won.
    teamsLeft = teamsLeft.filter(tId => tId !== teamId);
    if (!winningTeamId && teamsLeft.length == 1) {
      winningTeamId = teamsLeft[0];
      winningTeamConfirmed = !saverLeft;
    }
  }

  if (l.playerId == replaySaverPlayerId) {
    saverLeft = true;
    // If the saver left with only 2 teams remaining, the other team probably won.
    const teamsLeftGuess = teamsLeft.filter(t => t !== playerTeams[l.playerId]);
    if (teamsLeftGuess.length == 1) {
      winningTeamId = teamsLeftGuess[0];
    }
  }
});

// Some players are incorrectly marked as "left" when they stayed til the end, patch it up
let lastLeaveMs = null;
let loserLeft = false;
if (winningTeamId !== null) {
  for (let i = leaveEvents.length - 1; i > 0; --i) {
    const { playerId, ms, reason } = leaveEvents[i];
    const teamId = playerTeams[playerId];
    const isWinner = teamId == winningTeamId;
    if (reason == 'gameEnd') {
      lastLeaveMs = ms;
      if (!isWinner) loserLeft = true;
    } else if (isWinner && (ms == lastLeaveMs || !loserLeft)) {
      leaveEvents[i].reason = 'gameEnd';
    } else {
      break;
    }
  }
}

replay.saverPlayerId = replaySaverPlayerId;
replay.winningTeamId = winningTeamId;
replay.winningTeamConfirmed = winningTeamConfirmed;
replay.leaveEvents = leaveEvents;
replay.tradeEvents = tradeEvents;

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

  // Add ally options event (shared control)
  p['allyOptions'] = playerShareEvents[p['id']]
    ? playerShareEvents[p['id']]
    : [];
});

writeFileSync(outputPath, JSON.stringify(replay));
return 0;