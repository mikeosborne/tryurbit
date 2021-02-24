create table comet_status (
    status int
  , name varchar(64)
);

insert into comet_status values (0, 'DROPPED');
insert into comet_status values (1, 'MINED');
insert into comet_status values (2, 'CODE');
insert into comet_status values (3, 'READY');
insert into comet_status values (4, 'ASSIGNED');
