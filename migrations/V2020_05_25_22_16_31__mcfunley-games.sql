-- -*- sql-dialect: postgres; -*-
create view ladder_1v1 as
select * from games where is_ladder and type='1v1';


create view mcfunley as
select * from players where name='mcfunley';
