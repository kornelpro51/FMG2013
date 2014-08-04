#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from leads.views.manager import IndexView, AgentSetupView, LeadSourceView, ScheduleView, AlertView, GoalView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='manager-dashboard',),
                       url(r'^agents/$', AgentSetupView.as_view(), name='manager-agents',),
                       url(r'^leads/$', LeadSourceView.as_view(), name='manager-sources',),
                       url(r'^schedule/$', ScheduleView.as_view(), name='manager-schedule',),
                       url(r'^alerts/$', AlertView.as_view(), name='manager-alert',),
                       url(r'^goals/$', GoalView.as_view(), name='manager-alert',),
                       )