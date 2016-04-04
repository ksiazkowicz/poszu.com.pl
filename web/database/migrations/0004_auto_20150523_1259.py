# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20150523_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='Nazwa',
        ),
        migrations.RemoveField(
            model_name='item',
            name='Opis',
        ),
        migrations.RemoveField(
            model_name='item',
            name='Pozycja X',
        ),
        migrations.RemoveField(
            model_name='item',
            name='Pozycja Y',
        ),
        migrations.RemoveField(
            model_name='item',
            name='Zdjecie',
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='', max_length=300, verbose_name='Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='loc_latitude',
            field=models.FloatField(default=0, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='item',
            name='loc_longitude',
            field=models.FloatField(default=0, verbose_name='Longitude'),
        ),
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.CharField(default='', max_length=128, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='photo',
            field=models.ImageField(default='', upload_to=b'item/photos', verbose_name='Photo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='upload_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Uploaded date'),
        ),
    ]
