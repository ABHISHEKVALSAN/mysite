#pollSite 

from __future__ import unicode_literals
from django.contrib import admin

from .models import PageUrl, Choice

admin.site.register(PageUrl)
admin.site.register(Choice)


