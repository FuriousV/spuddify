from django.conf.urls import *
from django.conf import settings
from spuddify import views

urlpatterns = patterns('',
    url(r'^$', views.list_articles),
    url(r'^articles$', views.list_articles),
    url(r'^articles/create$', views.create_article),
    url(r'^articles/(?P<article_id>\w*)$', views.article_detail),
    url(r'^articles/(?P<article_id>\w*)/edit$', views.edit_article),
    url(r'^articles/(?P<article_id>\w*)/delete$', views.delete_article),
    url(r'^reset$', views.reset),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    )