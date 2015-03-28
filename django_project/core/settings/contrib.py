# -*- coding: utf-8 -*-
from .base import *

# Extra installed apps
INSTALLED_APPS += (
    # 'raven.contrib.django',  # enable Raven plugin
    'pipeline',
    'registration'
)

# define template function (example for underscore)
# PIPELINE_TEMPLATE_FUNC = '_.template'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder'
)

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
