# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20150523_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='email',
            field=models.CharField(default='', max_length=128, verbose_name='E-Mail'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='hash',
            field=models.CharField(default='', max_length=256, verbose_name='Hash'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'media/photos', verbose_name='Photo'),
        ),
    ]
