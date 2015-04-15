# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cntapp', '0002_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.CharField(max_length=250, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(null=True, upload_to=''),
            preserve_default=True,
        ),
    ]
