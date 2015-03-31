# -*- coding: utf-8 -*-
from .contrib import *

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # Or path to database file if using sqlite3.
        'NAME': '',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-5exebv4ni-9voevd0mnooc025r3pgo39'
MAILGUN_SERVER_NAME = 'sandboxff50038ad587497581376cc3e5b881de.mailgun.org'

# Project apps
INSTALLED_APPS += (
    'web',
    'accounts'
)


PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/jquery.min.js',
            'js/underscore.min.js',
            'js/foundation.min.js',
            'js/csrf-ajax.js',
            'js/leaflet.draw.js',
            'js/wicket.js',
            'js/wicket-leaflet.js',
            'js/app.js',
        ),
        'output_filename': 'js/contrib.js',
    },
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/normalize.css',
            'css/foundation.min.css',
            'css/foundation-icons/foundation-icons.css',
            'css/leaflet.draw.css',
            'css/main.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    },
}


# Django-registration settings
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'

# Email from wich messages are sent to users who requested address from widget.
FROM_EMAIL_ADDRESS_WIDGET = 'cropalert@cropalert.com'
