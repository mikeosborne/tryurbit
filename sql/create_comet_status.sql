create table comet_status (
    status int
  , name varchar(64)
);

insert into comet_status values (1, 'READY');
insert into comet_status values (2, 'ASSIGNED');
insert into comet_status values (3, 'DROPPED');
