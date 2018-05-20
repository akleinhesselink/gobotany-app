# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-19 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20180509_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='unit',
            field=models.CharField(blank=True, choices=[('m', 'Meters'), ('cm', 'Centimeters'), ('mm', 'Millimeters')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='value_type',
            field=models.CharField(choices=[('RATIO', 'Ratio'), ('TEXT', 'Textual'), ('LENGTH', 'Length')], max_length=10),
        ),
    ]