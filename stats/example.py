""" Crunch some data with Replay objects """
from collections import defaultdict
import loader


first_replay = loader.get_replay(1)
saver = first_replay.replay_saver()

print(f"First replay saved by {saver['name']}")

unit_counts = defaultdict(int)
for replay in loader.get_all_replays():
    for player in replay.players:
        for (unit, count) in player['units']['summary'].items():
            unit_counts[unit] += count

print(f"A total of {unit_counts['hpea']} peasants have been made")
