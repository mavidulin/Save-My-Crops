# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_alerts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alerts',
            name='crop_field',
        ),
        migrations.RemoveField(
            model_name='alerts',
            name='entry',
        ),
        migrations.RemoveField(
            model_name='alerts',
            name='user',
        ),
        migrations.DeleteModel(
            name='Alerts',
        ),
    ]
