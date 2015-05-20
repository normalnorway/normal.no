# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0002_auto_20150307_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(max_length=512, unique=True, null=True),
        ),
    ]
