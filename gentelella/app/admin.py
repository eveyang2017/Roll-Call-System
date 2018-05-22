from django.contrib import admin
from .models import User, Dictionary, DictionaryDetail, Course
# Register your models here.

admin.site.register(User)
admin.site.register(Dictionary)
admin.site.register(DictionaryDetail)
admin.site.register(Course)
