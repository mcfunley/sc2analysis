#!/usr/bin/env python
from argparse import ArgumentParser
from collections import defaultdict
import os
from getpass import getuser
from pathlib import Path
import json
import mpyq
import sc2reader
import pugsql


class UnitCollector(object):
    name = 'UnitCollector'

    def handleInitGame(self, event, replay):
        def blank():
            return {
                'born_frame': None, 'alive_frame': None, 'init_frame': None,
                'died_frame': None,
            }

        replay.unitargs = defaultdict(blank)
        replay.type_changes = []

    def handleUnitTypeChangeEvent(self, event, replay):
        replay.type_changes.append({
            'unit_id': event.unit_id_index,
            'recycle_id': event.unit_id_recycle,
            'frame': event.frame,
            'unit_type_name': event.unit_type_name,
        })

    def handleUnitBornEvent(self, event, replay):
        replay.unitargs[event.unit_id_index].update({
            'unit_id': event.unit_id_index,
            'born_frame': event.frame,
            'controlled_by_player_id': event.control_pid or None,
        })
        self.visit(event, replay, event.unit)

    def handleUnitInitEvent(self, event, replay):
        replay.unitargs[event.unit_id_index].update({
            'unit_id': event.unit_id_index,
            'init_frame': event.frame,
            'controlled_by_player_id': event.control_pid or None,
        })
        self.visit(event, replay, event.unit)

    def handleUnitDiedEvent(self, event, replay):
        replay.unitargs[event.unit_id_index].update({
            'unit_id': event.unit_id_index,
            'died_frame': event.frame,
        })
        self.visit(event, replay, event.unit)

    def visit(self, event, replay, u):
        replay.unitargs[event.unit_id_index].update({
            'owned_by_player_id': u.owner.pid if u.owner else None,
            'killed_by_player_id': u.killing_player.pid if u.killing_player else None,
            'killed_by_unit_id': u.killing_unit.id >> 18 if u.killing_unit else None,
            'minerals': u.minerals,
            'vespene': u.vespene,
            'hallucinated': u.hallucinated,
            'name': u.name,
            'supply': u.supply,
            'is_worker': u.is_worker,
            'is_army': u.is_army,
            'is_building': u.is_building,
            'race': u.race,
        })


sc2reader.engine.register_plugin(UnitCollector())

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

        for u in r.unitargs.values():
            u['game_id'] = game_id
            u['alive_frame'] = u['born_frame'] or u['init_frame'] or 0
            queries.create_unit(**u)

        for c in r.type_changes:
            c['game_id'] = game_id
            queries.create_unit_type_change(**c)


def main():
    ap = ArgumentParser()
    ap.add_argument('--one', action='store_true', default=False)
    args = ap.parse_args()

    for r in replays:
        parse(r)

        if args.one:
            break



if __name__ == '__main__':
    main()
