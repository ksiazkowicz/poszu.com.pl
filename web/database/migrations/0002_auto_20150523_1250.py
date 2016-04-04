# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Pozycja X',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='Pozycja Y',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='upload_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
