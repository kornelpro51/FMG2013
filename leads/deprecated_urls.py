from __future__ import unicode_literals
from django.conf.urls import patterns, url

import leads.views

urlpatterns = patterns('',
                       url(r'^customers/$', leads.views.CustomerList.as_view(), name='customer-list',),
                       url(r'^customers/(?P<pk>[0-9]+)/$', leads.views.CustomerDetail.as_view(), name='customer-detail',),
                       url(r'^properties/$', leads.views.PropertyList.as_view(), name='property-list',),
                       url(r'^properties/(?P<pk>[0-9]+)/$', leads.views.PropertyDetail.as_view(), name='property-detail',),
                       url(r'^for-current-month/$', leads.views.LeadListForCurrentMonth.as_view(), name='lead-for-current-month-list',),
                       url(r'^(?P<pk>[0-9]+)/$', leads.views.LeadDetail.as_view(), name='lead-detail',),
                       url(r'^notes-for-lead/(?P<pk>[0-9]+)/$', leads.views.NoteListForLead.as_view(), name='note-list-for-lead',),
                       url(r'^notes/(?P<pk>[0-9]+)/$', leads.views.NoteDetail.as_view(), name='note-detail',),
                       url(r'^messages-for-lead/(?P<pk>[0-9]+)/$', leads.views.MessageListForLead.as_view(), name='message-list-for-lead',),
                       url(r'^messages/(?P<pk>[0-9]+)/$', leads.views.MessageDetail.as_view(), name='message-detail',),


                       )
