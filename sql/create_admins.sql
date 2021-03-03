create table admins (
      name varchar(255)
    , email varchar(255)
    , notificaton_daily boolean
    , alert_low_mined boolean
    , alert_low_ready boolean
    , alert_max_users boolean
);

insert into admins values ("Mike", "mike@urbit.org", true, true, true, true);
insert into admins values ("Josh", "josh@urbit.org", true, false, false, false);

