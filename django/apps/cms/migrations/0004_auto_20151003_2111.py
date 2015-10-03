# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20150717_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='image',
            field=models.FileField(help_text=b'Image used when sharing the page on social media. When unset, Normals logo is used.', upload_to=b'cms/page', blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 3, 21, 11, 17, 206216), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='published',
            field=models.BooleanField(default=True, help_text=b'When unchekced the page is not globally accessible.'),
        ),
        migrations.AddField(
            model_name='page',
            name='summary',
            field=models.TextField(help_text=b'Short summary used when sharing the page on social media.', blank=True),
        ),
    ]
