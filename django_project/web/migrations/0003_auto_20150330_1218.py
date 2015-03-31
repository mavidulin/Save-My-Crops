# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20150330_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropfield',
            name='fertilizer_use',
            field=models.TextField(null=True, verbose_name=b'Fertilizer use', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cropfield',
            name='other_soil_parameters',
            field=models.TextField(null=True, verbose_name=b'Other Soil Parameters', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cropfield',
            name='pesticide_use',
            field=models.TextField(null=True, verbose_name=b'Pesticide use (includes: herbicide, insecticide,fungicide... and other)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cropfield',
            name='ph',
            field=models.IntegerField(null=True, verbose_name=b'Soil Ph level', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cropfield',
            name='soil_texture',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Soil Texture', blank=True),
            preserve_default=True,
        ),
    ]
