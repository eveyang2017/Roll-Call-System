# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-02 07:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180522_2128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u7ec4\u7ec7\u540d\u79f0')),
                ('pri', models.IntegerField(verbose_name='\u5e8f\u53f7')),
                ('desc', models.CharField(max_length=100, verbose_name='\u5907\u6ce8')),
                ('full_path', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u5168\u8def\u5f84')),
                ('deep_level', models.IntegerField(default=0, verbose_name='\u6df1\u5ea6')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='app.Department', verbose_name='\u4e0a\u7ea7\u7ed3\u6784')),
            ],
            options={
                'verbose_name': '\u7ec4\u7ec7\u7ed3\u6784',
                'verbose_name_plural': '\u7ec4\u7ec7\u7ed3\u6784',
            },
        ),
    ]
