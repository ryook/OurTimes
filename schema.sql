DROP table if exists entries;
create table entries (
	id integer primary key autoincrement,
	title string not null,
	member string not null,
	date string not null
);
