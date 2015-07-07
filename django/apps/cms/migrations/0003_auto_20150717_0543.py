# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'permissions': (('create_root_pages', 'Can create non-restricted page urls'),)},
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(unique=True, max_length=75),
        ),
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.CharField(unique=True, max_length=83, validators=[django.core.validators.RegexValidator(re.compile(b'^/(([-a-z0-9]+)/)+$'), 'Enter a valid url path consisting of letters, numbers or hyphens. It must begin and end with a slash.')]),
        ),
    ]
