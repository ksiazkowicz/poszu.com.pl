# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import osm_field.validators
import osm_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_item_is_open'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='loc_latitude',
        ),
        migrations.RemoveField(
            model_name='item',
            name='loc_longitude',
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=osm_field.fields.OSMField(default=0.0, lat_field='location_lat', lon_field='location_lon'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='location_lat',
            field=osm_field.fields.LatitudeField(default=0.0, validators=[osm_field.validators.validate_latitude]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='location_lon',
            field=osm_field.fields.LongitudeField(default=0.0, validators=[osm_field.validators.validate_longitude]),
            preserve_default=False,
        ),
    ]
