-- -*- sql-dialect: postgres; -*-

create table games (
  game_id bigserial not null primary key,
  start_time timestamp with time zone not null,
  fps real not null,
  category text not null,
  map_name text not null,
  release text,

  created timestamp with time zone not null default current_timestamp,
  updated timestamp with time zone not null default current_timestamp,

  unique(start_time)
);



create function sc2.set_updated() returns trigger
  language plpgsql as $$
  begin
    new.updated = now();
    return new;
  end;
$$;

create trigger sc2_games_updated
before update on sc2.games
for each row execute procedure sc2.set_updated();
