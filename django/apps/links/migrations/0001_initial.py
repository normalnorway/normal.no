# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'kategori',
                'verbose_name_plural': 'kategorier',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('text', models.TextField(verbose_name=b'description', blank=True)),
                ('lang', models.CharField(help_text=b'Use a two character language code to show a flag beside the entry.', max_length=2, blank=True)),
                ('comment', models.TextField(help_text=b'For internal use. Not shown on webpage.', blank=True)),
                ('category', models.ForeignKey(to='links.Category')),
            ],
            options={
                'verbose_name': 'lenke',
                'verbose_name_plural': 'lenker',
            },
            bases=(models.Model,),
        ),
    ]
