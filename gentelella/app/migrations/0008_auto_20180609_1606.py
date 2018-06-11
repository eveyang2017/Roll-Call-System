# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-09 08:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='deep_level',
        ),
        migrations.RemoveField(
            model_name='department',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='department',
            name='full_path',
        ),
        migrations.RemoveField(
            model_name='department',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='department',
            name='pri',
        ),
        migrations.AddField(
            model_name='department',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u5907\u6ce8'),
        ),
        migrations.AddField(
            model_name='department',
            name='domain',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u57df\u540d'),
        ),
        migrations.AddField(
            model_name='department',
            name='info',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='\u7ec4\u7ec7\u8bf4\u660e'),
        ),
        migrations.AddField(
            model_name='department',
            name='monitor_url',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u76d1\u63a7\u9875\u9762'),
        ),
        migrations.AddField(
            model_name='department',
            name='upper_business',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u4e0a\u5c42\u7ec4\u7ec7'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='\u7ec4\u7ec7\u540d\u79f0'),
        ),
    ]
