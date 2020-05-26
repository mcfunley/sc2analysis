-- -*- sql-dialect: postgres; -*-
create view winners as
select p.* from players p join teams t using (game_id, team_id) where t.winner;

create view ggs as
with ggs as (
  select c.game_id, c.player_id, frame, message, t.winner
  from sc2.chats c
  join sc2.players p using (game_id, player_id)
  join sc2.teams t using (game_id, team_id)
  where lower(trim(c.message)) in ('gg', 'g', 'wp', 'ggwp', 'gg wp')
),

-- first gg as winner
offensive_ggs as (
  select g.*
  from ggs g
  where g.winner and not exists (
    select 1
    from ggs g2
    where g2.game_id = g.game_id and g2.frame < g.frame and g2.player_id != g.player_id
  )
),

-- first gg as loser
conceding_ggs as (
  select g.*
  from ggs g
  where not g.winner and not exists (
    select 1
    from ggs g2
    where g2.game_id = g.game_id and g2.frame < g.frame and g2.player_id != g.player_id
  )
),

-- gg as winner, earlier gg from loser
reciprocating_ggs as (
  select g.*
  from ggs g
  where g.winner and exists (
    select 1
    from ggs g2
    where g2.game_id = g.game_id and g2.frame < g.frame and g2.player_id != g.player_id
  )
)

select
  g.game_id,
  g.player_id,
  g.frame,
  g.message,
  (off.game_id is not null) as is_offensive,
  (conc.game_id is not null) as is_conceding,
  (recip.game_id is not null) as is_reciprocating
from ggs g
left join offensive_ggs off using (game_id, player_id, frame)
left join conceding_ggs conc using (game_id, player_id, frame)
left join reciprocating_ggs recip using (game_id, player_id, frame);
