#!/usr/bin/env python
import os
from getpass import getuser
from pathlib import Path
import sc2reader
import pugsql


queries = pugsql.module('sql/')
queries.connect('postgresql+pg8000://%s@127.0.0.1:5432/sc2' % getuser())


sc2dir = os.path.expanduser(
    '~/Library/Application Support/Blizzard/Starcraft II')
replays = Path(sc2dir).rglob('*.SC2Replay')


def one_replay():
    for p in replays:
        return sc2reader.load_replay(str(p), load_level=4)


def parse(r):
    print(f'Parsing {r.filename}')
    with queries.transaction():
        game_id = queries.create_game(
            start_time=r.start_time,
            fps=r.game_fps,
            category=r.category,
            map_name=r.map_name,
            release=r.release_string)

        for p in r.people:
            queries.create_person(
                game_id=game_id,
                person_id=p.pid,
                name=p.name,
                color=int(p.color.hex, 16),
                color_name=p.color.name,
                is_human=p.is_human,
                highest_league=p.highest_league,
                play_race=p.play_race)



if __name__ == '__main__':
    parse(one_replay())
