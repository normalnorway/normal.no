# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20150516_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(max_length=255, unique=True, null=True),
        ),
    ]
