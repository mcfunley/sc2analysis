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


create table people (
  game_id bigint not null references games (game_id),
  person_id bigint not null,

  name text not null,
  color integer not null,
  color_name text not null,
  is_human boolean not null,
  highest_league integer not null,
  play_race text not null,

  primary key(game_id, person_id)
);
