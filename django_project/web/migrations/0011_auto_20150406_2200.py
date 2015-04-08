# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20150331_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cropfield',
            name='additional_info',
            field=models.TextField(null=True, verbose_name=b'ADDITIONAL INFORMATION', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cropfield',
            name='crop_name',
            field=models.CharField(max_length=250, verbose_name=b'CROP NAME'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cropfield',
            name='fertilizer_use',
            field=models.TextField(null=True, verbose_name=b'FERTILIZER USE', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cropfield',
            name='other_soil_parameters',
            field=models.TextField(null=True, verbose_name=b'OTHER SOIL PARAMETERS', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cropfield',
            name='pesticide_use',
            field=models.TextField(null=True, verbose_name=b'PESTICIDE USE (includes: herbicide, insecticide,fungicide... and other)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cropfield',
            name='ph',
            field=models.IntegerField(null=True, verbose_name=b'SOIL PH LEVEL', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cropfield',
            name='planting_date',
            field=models.DateField(null=True, verbose_name=b'PLANTING DATE', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cropfield',
            name='soil_texture',
            field=models.CharField(max_length=500, null=True, verbose_name=b'SOIL TEXTURE', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='additional_info',
            field=models.TextField(null=True, verbose_name=b'ADDITIONAL INFORMATION', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='crop_field',
            field=models.ForeignKey(related_name='entries', verbose_name=b'CROP FIELD', blank=True, to='web.CropField', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='damage_estimation',
            field=models.IntegerField(null=True, verbose_name=b'ESTIMATION OF AFFECTED AREA IN PERCENTAGE (%)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='entry_type',
            field=models.CharField(max_length=250, verbose_name=b'PEST OR DISEASE?', choices=[(b'1', b'Pest'), (b'2', b'Disease'), (b'3', b'unknown')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='harvest_date',
            field=models.DateField(null=True, verbose_name=b'HARVEST DATE (required only if crop was harvested)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='harvest_destroyed',
            field=models.IntegerField(null=True, verbose_name=b'ESTIMATION OF PERCENTAGE OF DESTROYED HARVEST (%)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='is_harvested',
            field=models.BooleanField(default=False, verbose_name=b'IS CROP HARVESTED?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='occurence_date',
            field=models.DateField(verbose_name=b'DATE OF OCCURENCE'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='pest_disease_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'PEST OR DISEASE NAME', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='pesticide_use',
            field=models.TextField(null=True, verbose_name=b'PESTICIDE USE AND RESULTS', blank=True),
            preserve_default=True,
        ),
    ]
