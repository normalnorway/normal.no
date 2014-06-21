-- sqlite3 ../../db/normal.db < fixnews3.sql
-- BUG BUG BUG: fixnews[12] will swap date & pubdata. So fix it here.

.bail on
begin transaction;

alter table news_article rename to tmp;
create table news_article (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "date" date NOT NULL,
  "pubdate" date NOT NULL,
  "url" varchar(200) UNIQUE,
  "title" varchar(128) NOT NULL,
  "summary" text NOT NULL,
  "body" text
);
insert into news_article ("id", "date", "pubdate", "url", "title", "summary", "body")
  select id,pubdate,date,url,title,summary,body
  from tmp;
drop table tmp;

commit;
