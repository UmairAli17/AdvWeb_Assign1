# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='testing',
            field=models.CharField(default='test', max_length=4),
        ),
    ]
