# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-22 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_cs_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='dep',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u6240\u5c5e\u7ec4\u7ec7'),
        ),
    ]
