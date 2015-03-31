# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import topnotchdev.files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20150331_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='images',
            field=topnotchdev.files_widget.fields.ImagesField(default='static/img/no-thumb.png'),
            preserve_default=False,
        ),
    ]
