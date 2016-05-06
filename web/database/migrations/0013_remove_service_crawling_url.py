# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_service_crawling_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='crawling_url',
        ),
    ]
