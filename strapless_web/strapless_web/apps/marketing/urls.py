from __future__ import absolute_import

from django.conf.urls import patterns, url


urlpatterns = patterns('marketing.views',
    url(r'^$', 'homepage', {}, name='homepage'),
    url(r'^examples/$', 'examples', {}, name='examples'),
)
