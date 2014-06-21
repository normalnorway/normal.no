-- sqlite3 ../../db/normal.db < fixnews1.sql

.bail on
begin transaction;

-- "Alter" column url: allow NULL
alter table news_article rename to tmp;
create table news_article (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "date" date NOT NULL,
  "pubdate" date NOT NULL,
  "url" varchar(200) NULL,
  "title" varchar(128) NOT NULL,
  "summary" text NOT NULL,
  "body" text NULL
);
insert into news_article ("id", "date", "pubdate", "url", "title", "summary", "body")
  select *
  from tmp;
drop table tmp;

-- Blank string => NULL
update news_article set url=null where url='';

commit;
