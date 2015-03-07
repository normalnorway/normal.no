# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
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
            name='published',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='url_is_canonical',
            field=models.BooleanField(default=False, verbose_name=b'Is canonical?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(default='', help_text=b'Our comment to this news story. Usually empty.', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(help_text=b'Date of news article (url), not the day we posted it.', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='pubdate',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
