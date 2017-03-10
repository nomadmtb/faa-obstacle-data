# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Obstacle',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('type', models.CharField(max_length=25)),
                ('quantity', models.IntegerField()),
                ('agl_height', models.IntegerField()),
                ('amsl_height', models.IntegerField()),
                ('lighting', models.CharField(choices=[('R', 'Red'), ('D', 'Medium intensity White Strobe & Red'), ('H', 'High intensity White Strobe & Red'), ('M', 'Medium intensity White Strobe'), ('S', 'High intensity White Strobe'), ('F', 'Flood'), ('C', 'Duel Medium Catenary'), ('W', 'Synchronized Red Lighting'), ('L', 'Lighted (Type Unknown)'), ('N', 'None'), ('U', 'Unknown')], max_length=1)),
                ('horizontal_accuracy', models.IntegerField()),
                ('vertical_accuracy', models.IntegerField()),
                ('faa_study_id', models.CharField(max_length=250)),
                ('action', models.CharField(choices=[('A', 'Add'), ('C', 'Change'), ('D', 'Dismantle')], max_length=1)),
                ('action_date', models.DateTimeField()),
            ],
        ),
    ]
