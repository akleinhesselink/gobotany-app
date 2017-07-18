# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 18:47
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160413_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcecitation',
            name='publication_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(2017)], verbose_name='Publication Year'),
        ),
    ]
