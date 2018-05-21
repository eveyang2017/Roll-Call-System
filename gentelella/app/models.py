# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    num = models.CharField(max_length=32, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class Dictionary(models.Model):
    code = models.CharField(max_length=16)
    description = models.CharField(max_length=256)

    def __init__(self, *args, **kwargs):
        super(Dictionary, self).__init__(*args, **kwargs)
        self.headline = None

    def __str__(self):  # __unicode__ on Python 2
        return self.headline


class DictionaryDetail(models.Model):
    dictionary_id = models.IntegerField()
    item_key = models.IntegerField()
    item_value = models.CharField(max_length=32)
    is_default = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(DictionaryDetail, self).__init__(*args, **kwargs)
        self.headline = None

    def __str__(self):  # __unicode__ on Python 2
        return self.headline


# class Course(models.Model):
#     c_name = models.CharField(max_length=30)
#     c_desc = models.CharField(max_length=100)
#
#     class Meta:
#      db_table = 'course'


# class Profile(models.Model):
#     nickname = models.CharField(max_length=50, blank=True)
#     user = models.OneToOneField(User)

