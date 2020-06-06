create table images(
    id integer primary key,
    group_id integer,
    caption text,
    image blob
);

create table configs(
    id integer primary key,
    group_id integer,
    name varchar(255),
    value integer
);
