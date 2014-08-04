from __future__ import unicode_literals
from braces.views import LoginRequiredMixin
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormMixin
from django_filters import views as filter_views
import redis
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from agencies.models import Notification
from django_mailbox.models import Message
from leads.filters import LeadFilterSet
from leads.models import Lead
from fetchmyguest.utils.debug import tail
from fetchmyguest.utils.parse_email import check_email_for_lead
from leads.forms import EmailForm
from fetchmyguest.utils.redis_utils import get_redis_connection
import gevent
from json import loads, dumps
from leads.serializers import NotificationSerializer
from leads.sockets import get_room_chan_name

import logging

logger = logging.getLogger('')

class HomeView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if getattr(request.user, 'agent_profile', ''):
            return redirect(reverse('dashboard'))
        else:
            return super(HomeView, self).dispatch(request, *args, **kwargs)

class LeadFilterView(filter_views.FilterView):
    model = Lead
    filterset_class = LeadFilterSet
    template_name = 'leads/leads_filter.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'leads/dashboard.html'

class ParseEmail(LoginRequiredMixin ,DetailView):
    model = Message
    template_name = 'leads/parseemail.html'

    def get_context_data(self, **kwargs):
        context = super(ParseEmail, self).get_context_data(**kwargs)
        message = context['message']
        check_email_for_lead(message=message)


        return context

class ProcessEmail(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'leads/parseemail.html'

    def get_context_data(self, **kwargs):
        context = super(ProcessEmail, self).get_context_data(**kwargs)
        # from django_mailbox.models import Mailbox
        # mailbox = Mailbox.objects.get(pk=1)
        # message = context['message']
        # msg = mailbox._process_message(message.get_email_object())
        msg = self.object
        context['message'] = msg
        check_email_for_lead(message=msg)

        return context

class ReplyEmail(LoginRequiredMixin, FormMixin, DetailView):
    form_class = EmailForm
    template_name = 'leads/reply_email_form.html'
    model = Message
    context_object_name = 'message'
    success_url = '/'

    def get_object(self, queryset=None):
        obj = super(ReplyEmail, self).get_object(queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super(ReplyEmail,self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        return context
    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        from django.core.mail import EmailMultiAlternatives
        from fetchmyguest.utils.html2plaintext import html2plaintext
        import HTMLParser
        h = HTMLParser.HTMLParser()
        message = self.get_object()
        subject, to = 'Re: ' + message.subject, message.lead.customer.email
        html_content = h.unescape(form.cleaned_data['message'])
        text_content = html2plaintext(html_content)
        msg = EmailMultiAlternatives(subject, text_content,  [to])
        msg.attach_alternative(html_content, "text/html")
        sent_message = message.reply(msg)
        sent_message.lead = message.lead
        sent_message.save()
        return super(ReplyEmail,self).form_valid(form)



def pub(room, data):
    logger.debug('publishing')
    r = get_redis_connection()
    logger.debug('connecting')
    r.publish(room, data)


class AddAlert(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = 'leads/alert.html'


    def get_context_data(self, **kwargs):
        context = super(AddAlert, self).get_context_data(**kwargs)
        notification = context['notification']
        context['user'] = self.request.user
        ser = NotificationSerializer(instance=notification)
        data = JSONRenderer().render(ser.data)
        context['data'] = data
        r = get_redis_connection()
        room = get_room_chan_name(self.request.user)
        r.publish(room, data)
        return context

