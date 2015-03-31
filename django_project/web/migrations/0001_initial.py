# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CropField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crop_name', models.CharField(max_length=250, verbose_name=b'Crop Name')),
                ('planting_date', models.DateField(null=True, verbose_name=b'Planting Date', blank=True)),
                ('additional_info', models.TextField(null=True, verbose_name=b'Additional Info', blank=True)),
                ('area', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('date_added', models.DateField(null=True, verbose_name=b'Date Added', blank=True)),
                ('creator', models.ForeignKey(related_name='crop_fields', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pest_disease_name', models.CharField(max_length=250, null=True, verbose_name=b'Pest or Disease Name', blank=True)),
                ('entry_type', models.CharField(max_length=250, verbose_name=b'Pest or Disease?', choices=[(b'1', b'Pest'), (b'2', b'Disease'), (b'3', b'unknown')])),
                ('occurence_date', models.DateField(verbose_name=b'Date of Occurence')),
                ('damage_estimation', models.IntegerField(null=True, verbose_name=b'Estimation of affected area in percentage (%)', blank=True)),
                ('is_harvested', models.BooleanField(default=False, verbose_name=b'Is Crop Harvested?')),
                ('harvest_date', models.DateField(null=True, verbose_name=b'Harvest Date (required only if crop was harvested)', blank=True)),
                ('harvest_destroyed', models.IntegerField(null=True, verbose_name=b'Estimation of percentage of destroyed harvest (%)', blank=True)),
                ('additional_info', models.TextField(null=True, verbose_name=b'Additional Info', blank=True)),
                ('area', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('date_added', models.DateField(null=True, verbose_name=b'Date Added', blank=True)),
                ('creator', models.ForeignKey(related_name='entries', to=settings.AUTH_USER_MODEL)),
                ('crop_field', models.ForeignKey(related_name='entries', verbose_name=b'Crop Field', to='web.CropField')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
