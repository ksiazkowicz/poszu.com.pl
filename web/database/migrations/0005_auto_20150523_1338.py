# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20150523_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_lost',
            field=models.BooleanField(default=False, verbose_name='Is a lost object'),
        ),
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(upload_to=b'/static/item/photos', verbose_name='Photo'),
        ),
    ]
