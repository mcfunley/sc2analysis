-- -*- sql-dialect: postgres; -*-
create table units (
  game_id bigint not null references games (game_id),
  unit_id bigint not null,

  alive_frame bigint not null,
  init_frame bigint,
  born_frame bigint,
  died_frame bigint,

  controlled_by_player_id bigint,
  owned_by_player_id bigint,

  killed_by_player_id bigint,
  killed_by_unit_id bigint,

  minerals integer not null,
  vespene integer not null,
  hallucinated boolean not null default false,
  name text not null,
  supply integer not null,
  is_worker boolean not null,
  is_army boolean not null,
  is_building boolean not null,
  race text not null,

  primary key (game_id, unit_id),
  foreign key (game_id, killed_by_unit_id) references units (game_id, unit_id) deferrable initially deferred,
  foreign key (game_id, killed_by_player_id) references players (game_id, player_id),
  foreign key (game_id, controlled_by_player_id) references players (game_id, player_id),
  foreign key (game_id, owned_by_player_id) references players (game_id, player_id),
  check(init_frame is not null or born_frame is not null)
);

create table unit_type_changes (
  game_id bigint not null references games (game_id),
  unit_id bigint not null,
  recycle_id bigint not null,

  frame bigint not null,
  unit_type_name text not null,

  foreign key (game_id, unit_id) references units (game_id, unit_id),
  primary key (game_id, unit_id, recycle_id, frame)
);
