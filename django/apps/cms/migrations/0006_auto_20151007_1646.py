# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20151004_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='created',
            field=models.DateTimeField(default='2015-10-01 00:00:00', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='image_show',
            field=models.BooleanField(default=True, help_text=b'Show social-media image at top of the page.', verbose_name=b'Show image'),
        ),
    ]
