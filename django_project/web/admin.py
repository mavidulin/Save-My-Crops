# -*- coding: utf-8 -*-
from django.contrib.gis import admin

from .models import CropField, Entry

# admin.site.register(CropField)
admin.site.register(Entry)

admin.site.register(CropField, admin.GeoModelAdmin)
