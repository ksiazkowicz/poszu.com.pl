# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_auto_20160403_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Uploaded date')),
                ('last_attempt', models.DateTimeField(auto_now=True, verbose_name='Uploaded date')),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='source',
            field=models.CharField(default=b'poszu.com.pl', max_length=20, verbose_name='Source'),
        ),
    ]
