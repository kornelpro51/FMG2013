#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, url
from djrill.views import DjrillWebhookView


urlpatterns = patterns('',
                       url(r'^mandrill/$', DjrillWebhookView.as_view(), name='djrill_webhook'),
                       )
