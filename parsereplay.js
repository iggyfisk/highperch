const W3GReplay = require('w3gjs');
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

const replay = Parser.parse(inputPath);

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

// Clean double chats from replay saver, bug in Reforged beta, Blizzard may have fix it since
const sanitizedChat = [];
let lastSaverChatMs = 0;
let lastSaverChatMessage = null;
replay.chat.forEach(c => {
  const { playerId, timeMS, message} = c;
  if (playerId == replaySaverPlayerId) {
    if ((timeMS - lastSaverChatMs) < 500 && message == lastSaverChatMessage) {
      return;
    }
    lastSaverChatMs = timeMS;
    lastSaverChatMessage = message;
  }
  sanitizedChat.push(c);
});
replay.chat = sanitizedChat;

writeFileSync(outputPath, JSON.stringify(replay));
return 0;
