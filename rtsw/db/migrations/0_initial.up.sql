begin;

create table rtsw (
    time_tag timestamp primary key,
    propagated_time_tag timestamp not null,
    speed real not null,
    density real not null,
    temperature real not null,
    bx real,
    "by" real,
    bz real,
    bt real,
    vx real,
    vy real,
    vz real
);

commit;