create table comet (
    id int not null auto_increment
  , name varchar(64)
  , code varchar(64)
  , status int
  , pid int
  , port int
  , primary key (id)
);