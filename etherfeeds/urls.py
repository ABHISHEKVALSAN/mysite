from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from . import views
app_name = 'etherfeeds'
urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^action$',views.action,name='action'),
	url(r'^thanks$',views.thanks,name='thanks'),
]
