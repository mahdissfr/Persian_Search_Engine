from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'inforet'

urlpatterns = [
    # /music/
    url(r'^similarity/$', views.similarityHome, name='similarityHomepage'),
    url(r'^clustering/$', views.clusterHome, name='clusterHomepage'),
    url(r'^$', views.simpleHome, name='simpleHomepage'),
    url(r'^similarity/searching/$', views.get_queryset_similarity, name='similarityIndex'),
    url(r'^clustering/searching/$', views.get_queryset_clustering, name='clusterIndex'),
    url(r'^searching/$', views.get_queryset, name='simpleIndex'),
    url(r'^searching/sort/$', views.time_sort, name='time_sort'),
    url(r'^searching/page=(?P<other_page>\w+)/$', views.get_other_page, name='other_page'),
    url(r'^searching/page=(?P<other_page>\w+)/$', views.get_other_page_cluster, name='other_page_cluster'),
    url(r'^news/(?P<doc_id>\w+)/$', views.get_news_url, name='news'),
]
