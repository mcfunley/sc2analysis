import os
from pathlib import Path
import sc2reader

sc2dir = os.path.expanduser(
    '~/Library/Application Support/Blizzard/Starcraft II')
replays = Path(sc2dir).rglob('*.SC2Replay')

def parse(fn):
    players, timeline, summary_stats, metadata = parse_replay(
        fn, local=False, detailed=True)
    return {
        'players': players,
        'timeline': timeline,
        'summary_stats': summary_stats,
        'metadata': metadata,
    }

def parseone():
    for p in replays:
        return sc2reader.load_replay(str(p), load_level=4)
