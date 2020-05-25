-- :name create_game :insert
insert into sc2.games (start_time, fps, category, map_name, release)
values (:start_time, :fps, :category, :map_name, :release)
on conflict(start_time) do update
  set fps = :fps,
      category = :category,
      map_name = :map_name,
      release = :release
returning game_id;

-- :name create_team :affected
insert into sc2.teams (game_id, team_id, winner)
values (:game_id, :team_id, :winner)
on conflict (game_id, team_id) do nothing;

-- :name create_player :affected
insert into sc2.players (
  game_id, player_id, name, color, color_name, is_human, highest_league, pick_race, play_race, url, team_id)
values (
  :game_id, :player_id, :name, :color, :color_name, :is_human, :highest_league, :pick_race, :play_race,
  :url, :team_id)
on conflict (game_id, player_id) do update
  set name = :name,
      color = :color,
      color_name = :color_name,
      is_human = :is_human,
      highest_league = :highest_league,
      pick_race = :pick_race,
      play_race = :play_race,
      url = :url,
      team_id = :team_id;
