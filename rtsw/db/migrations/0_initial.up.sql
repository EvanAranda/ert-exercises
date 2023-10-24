begin;

create table rtsw (
    time_tag timestamp primary key,
    propagated_time_tag timestamp not null,
    speed double precision,
    density double precision,
    temperature double precision,
    bx double precision,
    "by" double precision,
    bz double precision,
    bt double precision,
    vx double precision,
    vy double precision,
    vz double precision
);

commit;