#!/usr/bin/env python
import os
from getpass import getuser
from pathlib import Path
import json
import mpyq
import sc2reader
import pugsql


queries = pugsql.module('sql/')
queries.connect('postgresql+pg8000://%s@127.0.0.1:5432/sc2' % getuser())


sc2dir = os.path.expanduser(
    '~/Library/Application Support/Blizzard/Starcraft II')
replay_files = Path(sc2dir).rglob('*.SC2Replay')
replays = (sc2reader.load_replay(str(p), load_level=4) for p in replay_files)

def one_replay():
    for r in replays:
        return r


def parse(r):
    print(f'Parsing {r.filename}')

    mpq = mpyq.MPQArchive(r.filename)
    metadata = json.loads(
        mpq.read_file('replay.gamemetadata.json').decode('utf8'))

    playermeta = { d['PlayerID']: d for d in metadata['Players'] }

    with queries.transaction():
        game_id = queries.create_game(
            start_time=r.start_time,
            fps=r.game_fps,
            category=r.category,
            map_name=r.map_name,
            release=r.release_string,
            type=r.game_type,
            length_seconds=int(r.length.total_seconds()),
            is_ladder=r.is_ladder,
            is_private=r.is_private,
            region=r.region,
            speed=r.speed)

        for t in r.teams:
            queries.create_team(
                game_id=game_id,
                team_id=t.number,
                winner=r.winner.number == t.number)

        for p in r.players:
            pm = playermeta[p.pid]
            queries.create_player(
                game_id=game_id,
                player_id=p.pid,
                name=p.name,
                color=int(p.color.hex, 16),
                color_name=p.color.name,
                is_human=p.is_human,
                highest_league=getattr(p, 'highest_league', None),
                pick_race=p.pick_race,
                play_race=p.play_race,
                url=getattr(p, 'url', None),
                team_id=p.team_id,
                mmr=int(pm['MMR']) if 'MMR' in pm else None,
                apm=int(pm['APM']))

        for m in r.messages:
            if hasattr(m, 'text'):
                queries.create_chat(
                    game_id=game_id,
                    player_id=m.player.pid,
                    frame=m.frame,
                    second=m.second,
                    to_all=m.to_all,
                    to_allies=m.to_allies,
                    to_observers=m.to_observers,
                    message=m.text)



if __name__ == '__main__':
    for r in replays:
        parse(r)
