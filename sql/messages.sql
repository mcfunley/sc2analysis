-- :name create_message :affected
insert into sc2.messages (game_id, player_id, frame, second, to_all, to_allies, to_observers, message)
values (:game_id, :player_id, :frame, :second, :to_all, :to_allies, :to_observers, :message)
on conflict (game_id, player_id, frame) do update
  set second = :second,
      to_all = :to_all,
      to_allies = :to_allies,
      to_observers = :to_observers,
      message = :message;
