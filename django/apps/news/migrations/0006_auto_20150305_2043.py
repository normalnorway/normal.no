# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20150303_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, help_text=b'Date of news article (url), not the day we posted it.', null=True),
            preserve_default=True,
        ),
    ]
