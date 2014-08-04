from __future__ import unicode_literals
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView


import leads.views




urlpatterns = patterns('',
                       url(r'', include('leads.standard_urls')),
                       # url(r'', include('leads.deprecated_urls')),

                       )
