# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20150524_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='source',
            field=models.CharField(max_length=20, verbose_name='Source', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='url',
            field=models.CharField(max_length=400, verbose_name='URL', blank=True),
        ),
    ]
