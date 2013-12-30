from django.conf.urls import patterns, url

from nuvo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^source/$', views.model_list, { 'model_name': 'sources' } ),
    url(r'^source/(?P<source_name>\w[A-Za-z0-9_ ]*)/$', views.source, name='source_view'),
    url(r'^list/(?P<model_name>\w[A-Za-z0-9_ ]*)/$', views.model_list, name='model_list'),
    url(r'^(?P<zone_name>\w[A-Za-z0-9_ ]*)/$', views.zone, name='zone_view'),
)