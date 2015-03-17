# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=2, choices=[('v', 'video'), ('s', 'sound'), ('p', 'pdf'), ('i', 'image'), ('o', 'others')])),
                ('description', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubDirRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('child', models.ForeignKey(related_name='child', to='cntapp.Directory')),
                ('parent', models.ForeignKey(related_name='parent', to='cntapp.Directory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='directory',
            name='documents',
            field=models.ManyToManyField(to='cntapp.Document', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directory',
            name='sub_dirs',
            field=models.ManyToManyField(to='cntapp.Directory', through='cntapp.SubDirRelation', blank=True),
            preserve_default=True,
        ),
    ]
