#pollSite

from __future__ import unicode_literals
from django.contrib import admin

from .models import siteUrl, Person, Entries

admin.site.register(siteUrl)
admin.site.register(Person)
admin.site.register(Entries)
