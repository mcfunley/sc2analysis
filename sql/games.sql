-- :name create_game :affected
insert into sc2.games (start_time, fps, category, map_name, release)
values (:start_time, :fps, :category, :map_name, :release)
on conflict(start_time) do update
  set fps = :fps,
      category = :category,
      map_name = :map_name,
      release = :release;
