# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 17:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20170805_1753'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='book1',
            new_name='firstbook',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='book2',
            new_name='secondbook',
        ),
    ]
