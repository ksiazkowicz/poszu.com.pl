# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20160418_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='crawling_url',
            field=models.CharField(default='', max_length=128, verbose_name='URL'),
            preserve_default=False,
        ),
    ]
