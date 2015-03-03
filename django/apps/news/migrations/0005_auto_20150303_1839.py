# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20150303_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image_url',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='url_is_canonical',
            field=models.BooleanField(default=False, verbose_name=b'Is canonical?'),
            preserve_default=True,
        ),
    ]
