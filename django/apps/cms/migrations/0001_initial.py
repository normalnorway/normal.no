# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce4.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'cms/file')),
                ('name', models.CharField(unique=True, max_length=50, blank=True)),
                ('size', models.IntegerField(editable=False)),
                ('mimetype', models.CharField(max_length=50, editable=False, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=150)),
                ('title', models.CharField(max_length=75)),
                ('content', tinymce4.models.HtmlField()),
            ],
        ),
    ]
