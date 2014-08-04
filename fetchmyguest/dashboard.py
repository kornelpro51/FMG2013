"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'fetchmyguest.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Fetchmyguest'),
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    _('Main Apps'),
                    column=1,
                    collapsible=False,
                    models=('leads.*',),
                ),
            ]
        ))
        
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Configuration'),
            column=2,
            collapsible=True,
            children = [
                modules.AppList(
                    _('Agencies'),
                    column=1,
                    collapsible=False,
                    models=('agencies.*',),
                ),
                modules.AppList(
                   _('Users'),
                    column=1,
                    collapsible=False,
                    models=('django.contrib.*',),
                ),
                modules.AppList(
                   _('Cities'),
                    column=1,
                    collapsible=False,
                    models=('cities_light.*',),
                )
            ]
        ))
        self.children.append(modules.Group(
            _('Email'),
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    None,
                    column=1,
                    collapsible=False,
                    models=('django_mailbox.*',),
                ),
            ]
        ))

        self.children.append(modules.Group(
            _('Other Applications:'),
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    None,
                    collapsible=True,
                    column=1,
                    css_classes=('collapse closed',),
                    exclude=('django_mailbox.*',
                             'leads.*','agencies.*',
                             'django.contrib.*',
                             'cities_light.*',
                    ),
                )
            ]
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=3,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Regular Expressions Documentation'),
                    'url': 'http://www.regular-expressions.info/reference.html',
                    'external': True,
                },
                {
                    'title': _('Django REST framework'),
                    'url': 'http://django-rest-framework.org/',
                    'external': True,
                },
                {
                    'title': _('Kendo UI Docs'),
                    'url': 'http://docs.kendoui.com//',
                    'external': True,
                },
            ]
        ))
        
        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            column=3,
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


