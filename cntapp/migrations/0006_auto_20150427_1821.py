# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cntapp', '0005_document_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to='thumbnails', blank=True),
            preserve_default=True,
        ),
    ]
