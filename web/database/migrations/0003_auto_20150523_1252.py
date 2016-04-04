# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20150523_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user',
        ),
        migrations.RemoveField(
            model_name='item',
            name='user',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
