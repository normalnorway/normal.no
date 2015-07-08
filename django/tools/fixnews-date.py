"""
Convert news.Article.{date,pubdate} from DateField to DateTimeField

Before running this script, remember to:
1) Change the field type in the models.py
2) Change the field type in the database:
   a) ./manage.py makemigrations news
   b) ./manage.py migrate news

Old articles have time set to 00:00:00
"""

import sqlite3
from datetime import datetime
from django.db import transaction
from apps.news.models import Article

# Can't use Django ORM since it will return None for date fields.
cursor = sqlite3.connect ('/home/torkel/www/db/normal.db').cursor()


def get_dates (field):
    """Returns a dict mapping primary key to date value (unicode)"""
    dates = {}
    query = 'select %s from news_article where id=?' % field
    for pk in Article.objects.values_list('pk', flat=True):
        res = cursor.execute (query, [pk])
        dates[pk] = res.fetchone()[0]
    return dates


if __name__ == '__main__':
    dates = get_dates ('date')
    pubdates = get_dates ('pubdate')

    transaction.set_autocommit (False)  # begin transaction
    for obj in Article.objects.only ('pk', 'date', 'pubdate'):
        assert obj.date == None
        assert obj.pubdate == None
        obj.date = datetime.strptime (dates[obj.pk], '%Y-%m-%d')
        obj.pubdate = datetime.strptime (pubdates[obj.pk], '%Y-%m-%d')
        obj.save()

    transaction.commit()
    #transaction.rollback()
