from django.conf.urls import patterns, include, url
from django.contrib import admin
from domain import views, settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'domain.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url( r'^admin/', include( admin.site.urls ) ),
    url( r'^nuvo/', include( 'nuvo.urls', namespace='nuvo' ) ),
    url( r'^devdocs/jquery/', views.jquery, name='jquery' ),
)

show_indexes = False
if settings.DEBUG:
    show_indexes = True

urlpatterns += patterns( '',
    url( r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], 'django.views.static.serve', 
        kwargs = {'document_root': settings.BASE_DIR + settings.STATIC_URL, 'show_indexes': show_indexes} )
)
    