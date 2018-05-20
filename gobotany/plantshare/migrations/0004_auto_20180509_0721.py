# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-09 11:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plantshare', '0003_auto_20170717_1447'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='emailaddress',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='emailaddress',
            name='user',
        ),
        migrations.RemoveField(
            model_name='emailconfirmation',
            name='email_address',
        ),
        migrations.DeleteModel(
            name='EmailAddress',
        ),
        migrations.DeleteModel(
            name='EmailConfirmation',
        ),
    ]