# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dof', '0003_auto_20170311_0540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obstacle',
            name='horizontal_accuracy',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='obstacle',
            name='vertical_accuracy',
            field=models.FloatField(null=True),
        ),
    ]
