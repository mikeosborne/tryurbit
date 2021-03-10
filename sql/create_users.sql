create table users (
    id int not null auto_increment
  , name varchar(255)
  , email varchar(255)
  , init_group varchar(255)
  , optin boolean
  , primary key (id)
);