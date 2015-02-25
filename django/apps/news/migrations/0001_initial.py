# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pubdate', models.DateField(auto_now_add=True)),
                ('date', models.DateField(default=datetime.datetime.now, help_text=b'Date of news article (url), not the day we posted it.')),
                ('url', models.URLField(unique=True, null=True)),
                ('title', models.CharField(max_length=128)),
                ('summary', models.TextField(help_text='Just copy the "ingress" into this field.')),
                ('body', models.TextField(help_text=b'Our comment to this news story. Usually empty.', null=True, blank=True)),
            ],
            options={
                'get_latest_by': 'date',
                'verbose_name': 'nyhets-lenke',
                'verbose_name_plural': 'nyhets-lenker',
            },
            bases=(models.Model,),
        ),
    ]
