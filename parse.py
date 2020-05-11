import os
from pathlib import Path
from zephyrus_sc2_parser import parse_replay

sc2dir = os.path.expanduser(
    '~/Library/Application Support/Blizzard/Starcraft II')
replays = Path(sc2dir).rglob('*.SC2Replay')
