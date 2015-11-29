# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce4.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_info'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='info',
            options={'ordering': ('-date',), 'verbose_name_plural': 'Info'},
        ),
        migrations.AlterField(
            model_name='info',
            name='body',
            field=tinymce4.models.HtmlField(blank=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
