# -*- coding: utf-8 -*-
from django.contrib.gis import admin

from .models import CropField, Entry, Alert

admin.site.register(Entry)
admin.site.register(Alert)

admin.site.register(CropField, admin.GeoModelAdmin)
