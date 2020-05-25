#!/usr/bin/env python
import os
from getpass import getuser
from pathlib import Path
import sc2reader
import pugsql


queries = pugsql.module('sql/')
queries.connect('postgresql+pg8000://%s@127.0.0.1:5432/sc2' % getuser())


class ThirdNexusTracker(object):
    pass


sc2dir = os.path.expanduser(
    '~/Library/Application Support/Blizzard/Starcraft II')
replays = Path(sc2dir).rglob('*.SC2Replay')


def one_replay():
    for p in replays:
        return sc2reader.load_replay(str(p), load_level=4)


def parse(r):
    print(f'Parsing {r.filename}')
    with queries.transaction():
        queries.create_game(
            start_time=r.start_time,
            fps=r.game_fps,
            category=r.category,
            map_name=r.map_name,
            release=r.release_string)


if __name__ == '__main__':
    parse(one_replay())
