# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-22 18:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20171222_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='general_module',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 22, 20, 28, 34, 623825)),
        ),
    ]
