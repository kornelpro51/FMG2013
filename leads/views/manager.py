from __future__ import unicode_literals
import json
from braces.views import LoginRequiredMixin

from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.views.generic import TemplateView
from fetchmyguest.utils.time import get_month_day_range
from leads.models import Lead

from leads.sockets import get_room_chan_name
from django.conf import settings

import random

from django.utils import timezone


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = 'manager/summary.html'


    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        nb_element = 3
        TODAY = timezone.now()
        months = 3
        if months > 2:
            FROM = TODAY+relativedelta(months=-abs(months - 1))
        else:
            FROM = TODAY+relativedelta(months=-1)


        # Let's create the list of the months

        x_data = []
        month_days = []
        for d in list(rrule(MONTHLY,dtstart=FROM, count=months)):
            month_days.append(get_month_day_range(d))
            x_data.append(d.strftime('%B'))

        # We must obtain the lsit of sources of the whole period
        sources_ls = Lead.objects.filter(
            modified__range=(month_days[0][0], month_days[-1][-1])
        ).order_by('source').distinct('source').values('source')
        chart_data = {'x': []}
        extra_serie = {"tooltip": {"y_start": "Total ", "y_end": " leads"}}

        # let's populate the actuat data
        i = 1
        for source in sources_ls:
            serie = []
            for period in month_days:

                serie.append(
                    Lead.objects.filter(modified__range=period).filter(source__icontains=source['source']).count()
                )
            chart_data['y'+unicode(i)] = serie
            chart_data['name'+unicode(i)] = source['source']
            chart_data['extra'+unicode(i)] = extra_serie
            i += 1
        chart_data['x'] = [period[0].strftime('%B') for period in month_days]
        charttype = "multiBarChart"
        chartcontainer = 'multibarchart_container'  # container name

        data = {
            'charttype': charttype,
            'chartdata': chart_data,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            },

        }
        n_ctx = ctx.copy()
        n_ctx.update(data)

        return n_ctx


class AgentSetupView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/agents.html'


class LeadSourceView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/lead_source.html'


class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/schedule.html'


class AlertView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/alerts.html'


class GoalView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/goal.html'