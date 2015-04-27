# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cntapp', '0004_auto_20150410_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='thumbnail',
            field=models.FileField(null=True, upload_to='thumbnails', blank=True),
            preserve_default=True,
        ),
    ]
