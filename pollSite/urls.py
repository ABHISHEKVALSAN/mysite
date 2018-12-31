#pollSite

from django.conf.urls import url
from . import views

app_name = 'pollSite'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<siteId>[0-9]+)/vote/$', views.vote, name='vote'),
	url(r'newPerson',views.newPerson,name='newPerson'),
	url(r'register', views.register, name='register'),
    url(r'thanks', views.thanks, name='thanks'),
]
