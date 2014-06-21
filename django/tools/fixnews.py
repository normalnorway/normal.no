'''
Old website allowed empty and duplicate urls field. The new site don't!
This script find duplicated news-artices. It will not fix it for you.
'''

import sqlite3

db = sqlite3.connect ('../../db/normal.db')


def find_duplicates():
    data = dict()
    dups = list()
    cur = db.cursor()
    cur.execute ('select id,url from news_article')
    while True:
        row = cur.fetchone()
        if not row: break
        pk,url = row
        if data.has_key(url) and url:
            #print 'Duplicate', pk, data[url][0]
            dups.append ((pk, data[url][0]))
        else:
            data[url] = row
    return dups


for pk1,pk2 in find_duplicates():
    row1 = db.execute ('select id,url,title from news_article where id=?', (pk1,)).fetchone()
    row2 = db.execute ('select id,url,title from news_article where id=?', (pk2,)).fetchone()
    print pk1, row1[2].encode('utf-8'), 'http://dev.normal.no/admin/news/article/%s/' % (pk1,)
    print pk2, row2[2].encode('utf-8'), 'http://dev.normal.no/admin/news/article/%s/' % (pk2,)
    print '-----'
