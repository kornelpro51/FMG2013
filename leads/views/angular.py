#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
from braces.views import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView
from fetchmyguest.utils.time import get_month_day_range
from leads.models import Lead
from datetime import datetime
from leads.sockets import get_room_chan_name
from django.conf import settings


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/base.html'

    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, 'agent_profile', ''):
            return redirect(reverse('auth_login'))
        else:
            return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # ToDo: get target data from admin
        TARGET = settings.AGENCY_MONTH_TARGET
        TODAY = timezone.now().date()
        ctx = super(IndexView, self).get_context_data(**kwargs)
        month_modified_leads = Lead.objects.filter(modified__range=get_month_day_range(TODAY)).exclude(long_term=True)
        month_created_leads = Lead.objects.filter(created__range=get_month_day_range(TODAY)).exclude(long_term=True)
        month_booked_leads = Lead.objects.filter(booked=True,
                                                 booked_date__range=get_month_day_range(TODAY)
                                                ).exclude(long_term=True)
        init_val = dict(
            leads_in=month_created_leads.count(),
            follow_ups=month_modified_leads.filter(first_response=False,
                                                   second_response=False,
                                                   offer=False, hot=False,
                                                   booked=False).count(),
            hot=Lead.objects.filter(hot=True).exclude(long_term=True).count(),
            booked=month_booked_leads.count(),
            goal=(month_booked_leads.count() / TARGET),
            target=TARGET,
            agent=self.request.user.get_full_name(),
            room=get_room_chan_name(self.request.user)
        )
        ctx['init_val'] = json.dumps(init_val, cls=DjangoJSONEncoder)
        return ctx


class PartialView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        template_name = 'partials/' + self.kwargs['template_name']
        return [template_name]


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/base.html'

    def get_context_data(self, **kwargs):
        TARGET = settings.AGENCY_MONTH_TARGET
        TODAY = datetime.now().date()
        ctx = super(DashboardView, self).get_context_data(**kwargs)
        month_modified_leads = Lead.objects.filter(modified__range=get_month_day_range(TODAY)).exclude(long_term=True)
        month_created_leads = Lead.objects.filter(created__range=get_month_day_range(TODAY)).exclude(long_term=True)
        month_booked_leads = Lead.objects.filter(booked=True,
                                                 booked_date__range=get_month_day_range(TODAY)
                                                ).exclude(long_term=True)
        init_val = dict(
            leads_in=month_created_leads.count(),
            follow_ups=month_modified_leads.filter(first_response=False,
                                                   second_response=False,
                                                   offer=False, hot=False,
                                                   booked=False).count(),
            hot=Lead.objects.filter(hot=True).exclude(long_term=True).count(),
            booked=month_booked_leads.count(),
            goal=(month_booked_leads.count() / TARGET),
            target=TARGET,
            agent=self.request.user.get_full_name(),
            room=get_room_chan_name(self.request.user)
        )
        ctx['init_val'] = json.dumps(init_val, cls=DjangoJSONEncoder)
        return ctx
