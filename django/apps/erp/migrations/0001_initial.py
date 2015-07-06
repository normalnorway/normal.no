# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('sted', models.CharField(help_text=b'Where the person lives. City, etc.', max_length=64, blank=True)),
                ('phone', models.CharField(max_length=16, blank=True)),
                ('phone2', models.CharField(max_length=16, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('email2', models.EmailField(max_length=254, blank=True)),
                ('facebook', models.URLField(blank=True)),
                ('company', models.CharField(help_text=b'Company, organization, affiliation, etc.', max_length=64, blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ContactTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=80, blank=True)),
                ('text', models.TextField(blank=True)),
                ('owner', models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=80)),
                ('date', models.DateTimeField()),
                ('end', models.TimeField(help_text=b'End time', null=True, blank=True)),
                ('location', models.CharField(max_length=80, blank=True)),
                ('url', models.URLField(help_text=b'e.g., link to facebook event', blank=True)),
                ('note', models.TextField(blank=True)),
                ('alarm', models.IntegerField(help_text=b'Set alarm to this many days before the event', null=True, blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'Defaults to you', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReminderType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('done', models.BooleanField(default=False)),
                ('deadline', models.DateField(null=True, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('assigned_to', models.ForeignKey(blank=True, to='erp.Contact', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('created', models.DateField(auto_now=True)),
                ('priority', models.CharField(default=b'm', max_length=1, choices=[(b'!', b'ASAP'), (b'h', b'High'), (b'm', b'Medium'), (b'l', b'Low')])),
                ('status', models.CharField(default=b'0', max_length=1, choices=[(b'0', b'Not started'), (b'1', b'Done'), (b'2', b'Started'), (b'3', b'Postponed'), (b'4', b'Pending other')])),
                ('due', models.DateField(help_text=b'Date the task should be complete', null=True, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'Defaults to you', null=True)),
                ('pending', models.ForeignKey(blank=True, to='erp.Task', help_text=b'Task awaits completion of other task', null=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField()),
                ('created', models.DateField(auto_now=True)),
                ('task', models.ForeignKey(to='erp.Task')),
            ],
        ),
        migrations.AddField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(to='erp.Task'),
        ),
        migrations.AddField(
            model_name='reminder',
            name='task',
            field=models.ForeignKey(blank=True, to='erp.Task', help_text=b'Link reminder to task', null=True),
        ),
        migrations.AddField(
            model_name='reminder',
            name='type',
            field=models.ForeignKey(to='erp.ReminderType'),
        ),
        migrations.AddField(
            model_name='contact',
            name='tags',
            field=models.ManyToManyField(to='erp.ContactTag', blank=True),
        ),
    ]
