create table comet (
    id int not null auto_increment
  , name varchar(64)
  , code varchar(64)
  , status int
  , pier varchar(64)
  , assigned int
  , pid int
  , port int
  , mined_ts timestamp
  , ready_ts timestamp
  , assigned_ts timestamp
  , dropped_ts timestamp
  , primary key (id)
);

insert into comet(name, code, status) values ('test','test', 0);