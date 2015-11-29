# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce4.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20151007_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('body', tinymce4.models.HtmlField()),
                ('image', models.ImageField(upload_to=b'cms/info', blank=True)),
            ],
        ),
    ]
