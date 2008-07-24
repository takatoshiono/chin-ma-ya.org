create table areas (
    id integer not null,
    name varchar(16) not null,
    initial_words varchar(3) not null,
    url text not null,
    updated_at timestamp not null,
    created_at datetime not null,
    deleted_at datetime default null,
    primary key (id)
);

create table shops (
    id integer not null,
    area_id integer not null,
    name varchar(32) not null,
    address text not null,
    latitude varchar(16),
    longitude varchar(16),
    extra text not null default '',
    updated_at timestamp not null,
    created_at datetime not null,
    deleted_at datetime default null,
    primary key (id)
);

create table queue_shop (
    id integer not null,
    method varchar(8) not null, -- add, delete
    area_id integer not null,
    area_name varchar(16) not null,
    shop_id integer default null,
    shop_name varchar(32) not null,
    address text not null,
    latitude varchar(16),
    longitude varchar(16),
    extra text not null default '',
    created_at datetime not null,
    primary key (id)
);

