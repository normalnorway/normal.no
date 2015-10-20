# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20150520_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(help_text=b'Date of news article (url), not the day we posted it.', null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
