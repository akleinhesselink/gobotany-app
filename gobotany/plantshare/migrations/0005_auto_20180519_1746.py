# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-19 21:46


from django.db import migrations
import gobotany.plantshare.models
import imagekit.models.fields
import storages.backends.s3boto


class Migration(migrations.Migration):

    dependencies = [
        ('plantshare', '0004_auto_20180509_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenedimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(storage=storages.backends.s3boto.S3BotoStorage(bucket='newfs', location='/upload_images'), upload_to=gobotany.plantshare.models.rename_image_by_type),
        ),
    ]