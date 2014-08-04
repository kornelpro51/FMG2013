from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView
from mezzanine.core.views import direct_to_template
from registration.backends.default.views import EmailRegistrationView
import socketio.sdjango
from leads.views import HomeView
from leads.views.angular import *
from django.conf import settings
from djrill import DjrillAdminSite

admin.site = DjrillAdminSite()
admin.autodiscover()
socketio.sdjango.autodiscover()


urlpatterns = patterns(
    '',
    #url(r'^grappelli/', include('grappelli.urls')),
    # url(r'^', include(router.urls)),
    url(r"^socket\.io", include(socketio.sdjango.urls)),
    url(r'^api/', include('leads.api_urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^accounts/register/$', EmailRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # url("^$", "mezzanine.pages.view.page", {"slug": "/"}, name="home"),
    url(r"^$", HomeView.as_view(), name="home"),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^leads/', include('leads.urls')),
    # url(r'^$', IndexView.as_view(), name='index'),

    url(r'partials/(?P<template_name>.+\.html?$)', PartialView.as_view()),
    url(r'^simplechat/$', TemplateView.as_view(template_name='dashboard/simplechat.html'), name="chat"),
    #added by yousuf as base of html
    url(r'^dashboard/$', IndexView.as_view(), name='dashboard'),
    url(r'^simpliq/$', TemplateView.as_view(template_name='simpliq/index.html'), name="simpliq"),

    #added by yousuf, as base of manager's dashboard
    url(r'^manager/', DashboardView.as_view()),

    url(r'^$', RedirectView.as_view(url='/leads/', permanent=True), name='index'),
    url(r'^webhooks/', include('leads.webhooks_urls')),
)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )


urlpatterns += patterns('',
    url(r"^", include("mezzanine.urls")),
)