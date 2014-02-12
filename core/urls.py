from django.conf.urls import *
from django.conf import settings
from core import views

urlpatterns = patterns('',
    url(r'^$', views.hello_world, name='hello-world'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    )
