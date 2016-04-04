# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20150524_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_successful',
            field=models.BooleanField(default=False, verbose_name='Was a success?'),
        ),
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'media/photos', verbose_name='Photo', blank=True),
        ),
    ]
