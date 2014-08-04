from __future__ import unicode_literals
from rest_framework.routers import DefaultRouter
import leads.views
from django.conf.urls import patterns, url, include
router = DefaultRouter()

router.register(r'leads',  leads.views.LeadViewSet)
router.register(r'agencies',  leads.views.AgencyViewSet)
router.register(r'users',  leads.views.UsersViewSet)
router.register(r'agents',  leads.views.AgentsViewSet)
router.register(r'customers',  leads.views.CustomerViewSet)
router.register(r'messages',  leads.views.MessageViewSet)
router.register(r'properties',  leads.views.PropertyViewSet)
router.register(r'notifications',  leads.views.NotificationViewSet)
router.register(r'leadnotifications',  leads.views.NotificationLeadViewSet)
router.register(r'notes',  leads.views.NoteViewSet)
router.register(r'templates',  leads.views.EmailResponseViewSet)

#router.register(r'leadproperties',  api_views.LeadPropertyViewSet, base_name='api/leadproperties')

lead_detail = leads.views.LeadViewSet.as_view({
    'get': 'retrieve'
})
property_detail = leads.views.PropertyViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = patterns('',

    # url(r'^customers/$', api_views.CustomerListCreate.as_view()),
    # url(r'^customers/(?P<pk>[0-9]+)/$', api_views.CustomerDetail.as_view()),
    #url(r'^leads/$', api_views.LeadListCreate.as_view()),
    # url(r'^leads/(?P<pk>[0-9]+)/$', leads.views.LeadDetail.as_view(), name='lead-detail',),
    # url(r'^leads/(?P<pk>[0-9]+)/$', lead_detail, name='lead-detail',),
    # url(r'^properties/(?P<pk>[0-9]+)/$', property_detail, name='property-detail',),
    url(r'^reply/(?P<lead_pk>\d+)/(?P<msg_pk>\d+)/$', leads.views.ReplyMessage.as_view(), name='reply-message'),
    url(r'^leads/(?P<lead_pk>\d+)/properties/$', leads.views.LeadPropertyListCreate.as_view(), name='leadproperty-list'),
    url(r'^lead_property/(?P<pk>[0-9]+)/$', leads.views.LeadPropertyDetail.as_view(), name='leadproperty-detail'),
    url(r'^template/first_response/(?P<lead_pk>\d+)/$', leads.views.FirstResponseTemplate.as_view(), name='lead-first_response'),
    url(r'^template/second_response/(?P<lead_pk>\d+)/$', leads.views.SecondResponseTemplate.as_view(), name='lead-second_response'),
    url(r'^template/offer_response/(?P<lead_pk>\d+)/$', leads.views.OfferResponseTemplate.as_view(), name='lead-offer_response'),
    url(r'^template/concierge_response/(?P<lead_pk>\d+)/$', leads.views.ConciergeResponseTemplate.as_view(), name='lead-concierge_response'),
    url(r'^template/default_response/(?P<lead_pk>\d+)/$', leads.views.DefaultResponseTemplate.as_view(), name='default_response'),
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)