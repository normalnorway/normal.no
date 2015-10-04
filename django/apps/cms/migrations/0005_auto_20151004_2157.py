# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20151003_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='image_show',
            field=models.BooleanField(default=True, help_text=b'Show social-media image at top of the page.'),
        ),
        migrations.AddField(
            model_name='page',
            name='image_width',
            field=models.PositiveSmallIntegerField(help_text=b'Use this to override the image size.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='image',
            field=models.ImageField(help_text=b'Image used when sharing the page on social media. When unset, Normals logo is used.', upload_to=b'cms/page', blank=True),
        ),
    ]
