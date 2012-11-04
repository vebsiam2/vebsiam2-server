from django.conf.urls import patterns, include, url
from api import user
from server import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^user/', include('api.user')),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
                       
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^server/', include('server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
