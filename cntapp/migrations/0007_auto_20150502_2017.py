# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cntapp', '0006_auto_20150427_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.CharField(blank=True, choices=[('v', 'video'), ('a', 'sound'), ('p', 'pdf'), ('g', 'google_apk'), ('i', 'image'), ('o', 'others')], max_length=2),
            preserve_default=True,
        ),
    ]
