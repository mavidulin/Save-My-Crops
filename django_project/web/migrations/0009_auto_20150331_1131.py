# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import topnotchdev.files_widget.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20150330_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropfield',
            name='images',
            field=topnotchdev.files_widget.fields.ImagesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='images',
            field=topnotchdev.files_widget.fields.ImagesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='is_harvested',
            field=models.BooleanField(default=False, verbose_name=b'Is Crop Field Harvested?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
    ]
