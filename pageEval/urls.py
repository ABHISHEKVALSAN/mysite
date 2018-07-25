#pageEval


from . import views
from django.conf.urls import url
app_name = 'pageEval'
urlpatterns = [
    # ex: /pageEval/
    url(r'^$', views.index, name='index'),
    # ex: /pageEval/5/
    url(r'^detail/$', views.detail, name='detail'),
    # ex: /pageEval/5/results/
    url(r'^results/$', views.results, name='results'),
    # ex: /pageEval/5/vote/
    url(r'^metrics/$', views.metrics, name='metrics'),
    # url(r'^/vote/$', views.vote, name='vote'),
]
