# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 11:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20171222_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='general_module',
            name='time_on',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='general_module',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 28, 13, 41, 30, 51110)),
        ),
    ]