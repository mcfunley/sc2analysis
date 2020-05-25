-- -*- sql-dialect: postgres; -*-
create table chats (
  game_id bigint not null,
  player_id bigint not null,
  frame bigint not null,
  second integer not null,
  to_all boolean not null,
  to_allies boolean not null,
  to_observers boolean not null,
  message text,

  primary key (game_id, player_id, frame),
  foreign key (game_id, player_id) references players (game_id, player_id)
);
