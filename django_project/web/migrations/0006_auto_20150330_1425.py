# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20150330_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cropfield',
            name='date_added',
            field=models.DateField(auto_now_add=True, verbose_name=b'Date Added', null=True),
            preserve_default=True,
        ),
    ]
