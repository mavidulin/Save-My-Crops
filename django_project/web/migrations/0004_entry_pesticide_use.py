# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20150330_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='pesticide_use',
            field=models.TextField(null=True, verbose_name=b'Pesticide use and results', blank=True),
            preserve_default=True,
        ),
    ]
