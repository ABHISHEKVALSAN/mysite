from __future__ import unicode_literals
from django.contrib import admin

from .models import Users, HashList, Question, Choice

admin.site.register(Users)
admin.site.register(HashList)
admin.site.register(Question)
admin.site.register(Choice)
