-- :name create_game :insert
insert into sc2.games (start_time, fps, category, map_name, release)
values (:start_time, :fps, :category, :map_name, :release)
on conflict(start_time) do update
  set fps = :fps,
      category = :category,
      map_name = :map_name,
      release = :release
returning game_id;

-- :name create_person :affected
insert into sc2.people (
  game_id, person_id, name, color, color_name, is_human, highest_league, play_race)
values (:game_id, :person_id, :name, :color, :color_name, :is_human, :highest_league, :play_race)
on conflict (game_id, person_id) do update
  set name = :name,
      color = :color,
      color_name = :color_name,
      is_human = :is_human,
      highest_league = :highest_league,
      play_race = :play_race;
