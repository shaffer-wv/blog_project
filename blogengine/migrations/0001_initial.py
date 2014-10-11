# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=40, unique=True, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField()),
                ('text', models.TextField()),
                ('slug', models.SlugField(unique=True, max_length=40)),
                ('category', models.ForeignKey(blank=True, to='blogengine.Category', null=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=40, unique=True, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blogengine.Tag', null=True, blank=True),
            preserve_default=True,
        ),
    ]
