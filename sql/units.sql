-- :name create_unit :affected
insert into sc2.units (
  game_id, unit_id, alive_frame, init_frame, born_frame, died_frame, controlled_by_player_id,
  owned_by_player_id, killed_by_player_id, killed_by_unit_id, minerals, vespene, hallucinated,
  name, supply, is_worker, is_army, is_building, race)
values (
  :game_id, :unit_id, :alive_frame, :init_frame, :born_frame, :died_frame, :controlled_by_player_id,
  :owned_by_player_id, :killed_by_player_id, :killed_by_unit_id, :minerals, :vespene, :hallucinated,
  :name, :supply, :is_worker, :is_army, :is_building, :race)
on conflict (game_id, unit_id) do nothing;

-- :name create_unit_type_change :affected
insert into sc2.unit_type_changes (game_id, unit_id, recycle_id, frame, unit_type_name)
values (:game_id, :unit_id, :recycle_id, :frame, :unit_type_name)
on conflict (game_id, unit_id, recycle_id, frame) do nothing;
