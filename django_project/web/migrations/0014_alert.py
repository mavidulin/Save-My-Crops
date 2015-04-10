# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0013_auto_20150410_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_viewed', models.BooleanField(default=False)),
                ('creation_time', models.DateField(auto_now_add=True, null=True)),
                ('crop_field', models.ForeignKey(related_name='alerts', to='web.CropField')),
                ('entry', models.ForeignKey(related_name='alerts', to='web.Entry')),
                ('user', models.ForeignKey(related_name='alerts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
