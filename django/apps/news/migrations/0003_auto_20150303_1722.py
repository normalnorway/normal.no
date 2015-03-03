# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_article_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, help_text=b'Date of news article (url), not the day we posted it.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='pubdate',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
