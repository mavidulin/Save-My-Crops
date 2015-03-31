# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_cropfield_date_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='date_edited',
            field=models.DateField(auto_now=True, verbose_name=b'Date Edited', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='date_added',
            field=models.DateField(auto_now_add=True, verbose_name=b'Date Added', null=True),
            preserve_default=True,
        ),
    ]
