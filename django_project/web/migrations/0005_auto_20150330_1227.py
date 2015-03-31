# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_entry_pesticide_use'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='crop_field',
            field=models.ForeignKey(related_name='entries', verbose_name=b'Crop Field', blank=True, to='web.CropField', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, verbose_name=b'Location (only if Crop Field is not selected)', blank=True),
            preserve_default=True,
        ),
    ]
