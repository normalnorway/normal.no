# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'pubdate', models.DateField(auto_now_add=True, verbose_name=b'Date published')),
                (b'date', models.DateField(default=datetime.datetime(2014, 6, 1, 19, 2, 21, 100774), help_text=b'Date of news article (url), not the day we posted it.')),
                (b'url', models.URLField(unique=True)),
                (b'title', models.CharField(max_length=128)),
                (b'summary', models.TextField(help_text='Just copy the "ingress" into this field.')),
                (b'body', models.TextField(help_text=b'Our comment to this news story', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'date', models.DateField(default=datetime.datetime(2014, 6, 1, 19, 2, 21, 102003))),
                (b'published', models.BooleanField(default=True)),
                (b'title', models.CharField(max_length=100)),
                (b'abstract', models.TextField(blank=True)),
                (b'text', models.TextField(help_text=b'NOTE: Supports Markdown syntax. (<a href="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet" target="_blank">Se here for help.</a>)')),
                (b'image', models.ImageField(upload_to=b'images/news_story', blank=True)),
                (b'image_text', models.CharField(max_length=255, blank=True)),
                (b'image_align', models.CharField(default=b'r', max_length=1, choices=[(b'l', b'Left'), (b'r', b'Right')])),
                (b'comment', models.TextField(help_text=b'Internal comment. Not shown on the website.', blank=True)),
            ],
            options={
                'verbose_name_plural': b'stories',
            },
            bases=(models.Model,),
        ),
    ]
