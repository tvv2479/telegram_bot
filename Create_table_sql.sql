 
-- Создание таблицы для телеграм-бота
create table test_tele(
       order_id serial,
       user_id integer,
       date_insert date,
       price numeric,
       PRIMARY KEY (order_id)
       );
     
-- Создание таблицы для SuperSet
create table test_bi(
       date date,
       lvl_5 varchar(500),
       card_id integer,
       checks integer
       );

 




