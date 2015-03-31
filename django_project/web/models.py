# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.contrib.gis.db import models

from topnotchdev import files_widget

from django.contrib.auth.models import User


class CropField(models.Model):
    crop_name = models.CharField(
        null=False,
        blank=False,
        max_length=250,
        verbose_name='Crop Name'
    )
    area = models.PolygonField(
        srid=4326,
        null=False,
        blank=False
    )
    planting_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Planting Date'
    )
    ph = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Soil Ph level'
    )
    other_soil_parameters = models.TextField(
        null=True,
        blank=True,
        verbose_name='Other Soil Parameters'
    )
    soil_texture = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='Soil Texture'
    )
    fertilizer_use = models.TextField(
        null=True,
        blank=True,
        verbose_name='Fertilizer use'
    )
    pesticide_use = models.TextField(
        null=True,
        blank=True,
        verbose_name='Pesticide use (includes: herbicide, insecticide,' +
        'fungicide... and other)'
    )
    additional_info = models.TextField(
        null=True,
        blank=True,
        verbose_name='Additional Info'
    )
    images = files_widget.ImagesField(blank=True, null=True)

    date_added = models.DateField(
        null=True,
        blank=True,
        auto_now_add=True,
        verbose_name='Date Added'
    )
    date_edited = models.DateField(
        null=True,
        blank=True,
        auto_now=True,
        verbose_name='Date Edited'
    )
    creator = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='crop_fields'
    )

    objects = models.GeoManager()

    def __unicode__(self):
        return self.crop_name

    def as_geojson(self):
        return {
            'id': self.pk,
            'polygon': self.area.geojson,
        }

    def display_name(self):
        return self.crop_name + ' #' + str(self.id)


class Entry(models.Model):
    ENTRY_TYPE_CHOICES = (('1', 'Pest'), ('2', 'Disease'), ('3', 'unknown'))

    crop_field = models.ForeignKey(
        'CropField',
        null=True,
        blank=True,
        verbose_name='Crop Field',
        related_name='entries'
    )
    pest_disease_name = models.CharField(
        null=True,
        blank=True,
        max_length=250,
        verbose_name='Pest or Disease Name'
    )
    entry_type = models.CharField(
        null=False,
        blank=False,
        max_length=250,
        choices=(ENTRY_TYPE_CHOICES),
        verbose_name='Pest or Disease?'
    )
    occurence_date = models.DateField(
        null=False,
        blank=False,
        verbose_name='Date of Occurence'
    )
    damage_estimation = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Estimation of affected area in percentage (%)'
    )
    is_harvested = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name='Is Crop Field Harvested?'
    )
    harvest_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Harvest Date (required only if crop was harvested)'
    )
    harvest_destroyed = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Estimation of percentage of destroyed harvest (%)'
    )
    additional_info = models.TextField(
        null=True,
        blank=True,
        verbose_name='Additional Info'
    )
    pesticide_use = models.TextField(
        null=True,
        blank=True,
        verbose_name='Pesticide use and results'
    )
    images = files_widget.ImagesField(blank=False, null=False)

    location = models.PointField(
        srid=4326,
        null=True,
        blank=True,
    )

    date_added = models.DateField(
        null=True,
        blank=True,
        auto_now_add=True,
        verbose_name='Date Added'
    )
    date_edited = models.DateField(
        null=True,
        blank=True,
        auto_now=True,
        verbose_name='Date Edited'
    )
    creator = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='entries'
    )

    objects = models.GeoManager()

    def __unicode__(self):
        if self.crop_field:
            return self.crop_field.crop_name + ' incident'
        else:
            return 'individual incident'

    def as_geojson(self):
        return {
            'id': self.pk,
            'polygon': self.area.geojson,
        }
