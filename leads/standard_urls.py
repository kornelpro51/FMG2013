from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


import leads.views

urlpatterns = patterns('',
                       url(r'^$', leads.views.DashboardView.as_view(), name='leads-dashboard',),
                       url(r'^email/(?P<pk>[\d]+)/$', leads.views.ParseEmail.as_view(), name='parse-email'),
                       url(r'^process/(?P<pk>[\d]+)/$', leads.views.ProcessEmail.as_view(), name='process-email'),
                       url(r'^alert/(?P<pk>[\d]+)/$', leads.views.AddAlert.as_view(), name='add-alert'),
                       url(r'^new/', TemplateView.as_view(template_name = 'leads/simpledashboard.html' ), name='simpledash'),
                       url(r'^reply/(?P<pk>[\d]+)/$', leads.views.ReplyEmail.as_view(), name='reply-email'),
                       url(r'^filter/$', leads.views.LeadFilterView.as_view(), name='leads-filter')
)