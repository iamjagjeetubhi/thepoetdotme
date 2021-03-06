# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 13:58
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20170816_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='file',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='uploaded_images'),
        ),
    ]
