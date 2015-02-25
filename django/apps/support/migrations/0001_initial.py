# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('choice', models.CharField(max_length=1, verbose_name='Jeg \xf8nsker \xe5', choices=[(b'a', 'a) Nedkriminalisere cannabis (f.eks. etter Portugal-modellen).'), (b'b', 'b) Avkriminalisere cannabis for de over 18 \xe5r.'), (b'c', 'c) Avkriminalisere cannabis for de over 20 \xe5r.'), (b'd', 'd) Regulere cannabis. Staten tar seg av produksjon og distribusjon.')])),
                ('name', models.CharField(max_length=64, verbose_name='Navn')),
                ('city', models.CharField(max_length=64, verbose_name='Sted')),
                ('public', models.BooleanField(default=True, verbose_name='Vis mitt navn i listen under')),
            ],
            options={
                'ordering': ('-date',),
                'get_latest_by': 'date',
                'verbose_name': 'opprop',
                'verbose_name_plural': 'opprop',
            },
            bases=(models.Model,),
        ),
    ]
