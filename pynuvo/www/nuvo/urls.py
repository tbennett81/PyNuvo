from django.conf.urls import patterns, url

from nuvo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^sources/$', views.SourcesView.as_view(), name='sources'),
    url(r'^sources/(?P<source_number>\d+)/$', views.sourceDetail, name='sourceDetail'),
    url(r'^zones/$', views.zones, name='zones'),
    url(r'^zones/(?P<zone_number>\d+)/$', views.zoneDetail, name='zoneDetail'),
    url(r'^test/$', views.test, name='test' ),
)