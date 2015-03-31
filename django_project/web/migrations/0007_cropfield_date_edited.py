# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20150330_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropfield',
            name='date_edited',
            field=models.DateField(auto_now=True, verbose_name=b'Date Edited', null=True),
            preserve_default=True,
        ),
    ]
