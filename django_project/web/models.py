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
        verbose_name='CROP NAME'
    )
    area = models.PolygonField(
        srid=4326,
        null=False,
        blank=False
    )
    planting_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='PLANTING DATE'
    )
    ph = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='SOIL PH LEVEL'
    )
    other_soil_parameters = models.TextField(
        null=True,
        blank=True,
        verbose_name='OTHER SOIL PARAMETERS'
    )
    soil_texture = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='SOIL TEXTURE'
    )
    fertilizer_use = models.TextField(
        null=True,
        blank=True,
        verbose_name='FERTILIZER USE'
    )
    pesticide_use = models.TextField(
        null=True,
        blank=True,
        verbose_name='PESTICIDE USE (includes: herbicide, insecticide,' +
        'fungicide... and other)'
    )
    additional_info = models.TextField(
        null=True,
        blank=True,
        verbose_name='ADDITIONAL INFORMATION'
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
        verbose_name='CROP FIELD',
        related_name='entries'
    )
    pest_disease_name = models.CharField(
        null=True,
        blank=True,
        max_length=250,
        verbose_name='PEST OR DISEASE NAME'
    )
    entry_type = models.CharField(
        null=False,
        blank=False,
        max_length=250,
        choices=(ENTRY_TYPE_CHOICES),
        verbose_name='PEST OR DISEASE?'
    )
    occurence_date = models.DateField(
        null=False,
        blank=False,
        verbose_name='DATE OF OCCURENCE'
    )
    damage_estimation = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='ESTIMATION OF AFFECTED AREA IN PERCENTAGE (%)'
    )
    is_harvested = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name='IS CROP HARVESTED?'
    )
    harvest_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='HARVEST DATE (required only if crop was harvested)'
    )
    harvest_destroyed = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='ESTIMATION OF PERCENTAGE OF DESTROYED HARVEST (%)'
    )
    additional_info = models.TextField(
        null=True,
        blank=True,
        verbose_name='ADDITIONAL INFORMATION'
    )
    pesticide_use = models.TextField(
        null=True,
        blank=True,
        verbose_name='PESTICIDE USE AND RESULTS'
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


class Alert(models.Model):
    entry = models.ForeignKey(
        Entry,
        null=False,
        blank=False,
        related_name='alerts'
    )
    # Crop Field near entry
    crop_field = models.ForeignKey(
        CropField,
        null=False,
        blank=False,
        related_name='alerts'
    )
    # Crop Field Owner
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='alerts'
    )
    is_viewed = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    creation_time = models.DateField(
        null=True,
        blank=True,
        auto_now_add=True
    )

    def get_alert_css_class(self):
        if self.is_viewed is False:
            return 'new-alert'
        else:
            return 'old-alert'
