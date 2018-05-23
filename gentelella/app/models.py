# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, verbose_name="昵称")
    num = models.CharField(max_length=32, blank=True, verbose_name="工号")
    university = models.CharField(max_length=100, blank=True, verbose_name="学校")
    college = models.CharField(max_length=100, blank=True, verbose_name="学院")
    faculty = models.CharField(max_length=100, blank=True, verbose_name="系别")

    class Meta(AbstractUser.Meta):
        pass


class Dictionary(models.Model):
    code = models.CharField(max_length=16, verbose_name="编号")
    description = models.CharField(max_length=256, verbose_name="字典说明")

    class Meta:
        verbose_name = "数据字典"

    def __str__(self):  # __unicode__ on Python 2
        return self.code


class DictionaryDetail(models.Model):
    dictionary_id = models.IntegerField(verbose_name="字典编号")
    item_key = models.IntegerField(verbose_name="数据项键")
    item_value = models.CharField(max_length=32, verbose_name="数据项值")
    is_default = models.BooleanField(default=False, verbose_name="是否为默认")

    class Meta:
        verbose_name = "数据字典明细"

    def __str__(self):  # __unicode__ on Python 2
        return self.dictionary_id


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name="课程名称")
    category = models.CharField(max_length=30, blank=True, verbose_name="课程类别")
    credit = models.CharField(max_length=4, verbose_name="学分")
    hours = models.CharField(max_length=8, verbose_name="学时")
    teacher = models.CharField(max_length=10, blank=True, verbose_name="教师")
    desc = models.CharField(max_length=100, blank=True, verbose_name="课程说明")

    class Meta:
        verbose_name = "课程"

    def __str__(self):  # __unicode__ on Python 2
        return self.name


