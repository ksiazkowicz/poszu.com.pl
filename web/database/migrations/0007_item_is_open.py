# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20150524_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_open',
            field=models.BooleanField(default=True, verbose_name='Is open?'),
        ),
    ]
