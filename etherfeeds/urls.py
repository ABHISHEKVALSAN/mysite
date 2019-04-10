from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from . import views
app_name = 'etherfeeds'
urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'dashboard/',views.dashboard,name='dashboard'),
	url(r'createpoll/',views.createpoll,name='createpoll'),
	url(r'addmember/',views.addmember,name='addmember'),
	url(r'thanks/',views.thanks,name='thanks'),
]
