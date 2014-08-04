from __future__ import unicode_literals
import email
import rfc822
from cuser.middleware import CuserMiddleware
from custom_user.models import EmailUser
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives, make_msgid, EmailMessage
from django.db.models import Q
from django.http import Http404
from rest_framework import status, mixins, viewsets, generics, authentication, exceptions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_mailbox.models import Message
from events_logger.mandrill_utils import set_metadata
from fetchmyguest.utils.multiple_querysets import QuerySetSequence
from leads.filters import LeadFilterSet, MessageFilterSet, NotificationFilterSet, NoteFilterSet

from leads.models import Lead, LeadProperty, Note, Customer, Property, get_agency
from agencies.models import Notification, Agency, Agent
from leads import models, serializers
from leads.serializers import NotificationSerializer, ReplySerializer, EmailResponseSerializer, FirstResponseTemplateSerializer, SecondResponseTemplateSerializer, OfferResponseTemplateSerializer, ConciergeResponseTemplateSerializer, NoteSerializer, DefaultResponseTemplateSerializer, CustomerSerializer, MessageSerializer, ForwardSerializer
import warnings
import time
from django.core.signals import request_started, request_finished
import logging


logger = logging.getLogger('')
dispatch_time = 0
render_time = 0
started = 0
serializer_time = 0
db_time = 0
db_start = 0

class NoCacheModelViewSet(viewsets.ModelViewSet):

    @property
    def default_response_headers(self):

        return {
            'Allow': ', '.join(self.allowed_methods),
            'Vary': 'Accept',
            'Cache-Control': 'max-age=0, private, no-cache, no-store, must-revalidate, proxy-revalidate, no-transform'
        }


class CustomerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing customers.
    """
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

class AgencyViewSet(viewsets.ModelViewSet):
    model = Agency
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

class UsersViewSet(viewsets.ModelViewSet):
    model = EmailUser
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

class AgentsViewSet(viewsets.ModelViewSet):
    model = Agent
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

class PropertyViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing properties.
    """
    # queryset = Property.objects.all()
    serializer_class = serializers.PropertySerializer
    model = Property
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(PropertyViewSet, self).get_queryset()
        user = CuserMiddleware.get_user()
        if user:
            if user.is_superuser:
                return qs.filter(approved=True)
            else:
                return qs.filter(agency=get_agency(), approved=True)
        else:
            return qs.filter(agency=get_agency(), approved=True)


class LeadViewSet(NoCacheModelViewSet):
    """
    A simple ViewSet for viewing and editing Leads.

    ___Filtering___

    By default leads are filtered so as only the ones modified in the last 30 days are
    retrieved.

    The LeadFilterSet allow to search on the modified field by __DateRange__\n
    ?modified=6  Any date (All leads)\n
    ?modified=5  This year\n
    ?modified=4  This monthr\n
    ?modified=3  Past 30 days\n
    ?modified=2  Past 7 days\n
    ?modified=1  corresponds to today\n

    __Even ordering is available__\n
    ?ordering=-modified\n

    __Filtering__:\n
    this are the available filters\n
    ?leads_in=true\n
    ?follow_ups=true\n
    ?booked=true\n
    ?hot=true\n
    ?booked=true\n

    __Searching__:\n
    ?search=Mary\n
    Search fields available : 'customer\__first_name', 'customer\__last_name', 'customer\__email'
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LeadSerializer
    filter_class = LeadFilterSet
    model = Lead
    # ordering = ['-modified', '-hot', '-first_response', '-phone_call', '-created']
    search_fields = ('customer__first_name',
                     'customer__last_name',
                     'customer__email',
                     'properties__title',
                     'properties__address')


    def dispatch(self, request, *args, **kwargs):
        global dispatch_time
        global render_time
        dispatch_start = time.time()
        ret = super(LeadViewSet, self).dispatch(request, *args, **kwargs)
        render_start = time.time()
        ret.render()
        render_time = time.time() - render_start
        dispatch_time = time.time() - dispatch_start
        return ret


    def get_queryset(self):
        global db_start
        db_start = time.time()
        qs = Lead.objects.select_related('customer').all()
        source = self.request.QUERY_PARAMS.get('source', None)
        if source is not None:
            qs = qs.filter(source__icontains=source)
        user = CuserMiddleware.get_user()
        if user:
            if not user.is_superuser:
                qs = qs.filter(agency=get_agency())
        else:
            qs = qs.filter(agency=get_agency())
        return qs.distinct()

    def list(self, request, *args, **kwargs):
        global serializer_time
        global db_time
        query_params = request.QUERY_PARAMS.copy()
        qs = self.filter_queryset(self.get_queryset())
        qs1 = qs.filter(
            phone_call=False,
            first_response=False,
            second_response=False,
            offer=False,
            hot=False,
            booked=False,
            long_term=False
        ).order_by('created').prefetch_related('properties', 'customer', 'leadproperty_set')
        qs2 = qs.filter((
                            Q(phone_call=True) |
                            Q(first_response=True) |
                            Q(second_response=True) |
                            Q(offer=True) |
                            Q(hot=True)) &
                        (
                            Q(booked=False) &
                            Q(long_term=False)
                        )
        ).order_by('-hot', '-modified').prefetch_related( 'customer','properties', 'leadproperty_set')
        qs3 = qs.filter(
            long_term=True, booked=False
        ).order_by('-modified').prefetch_related('customer', 'properties', 'leadproperty_set')
        qs4 = qs.filter(
            booked=True
        ).order_by('-modified').prefetch_related('customer', 'properties', 'leadproperty_set')
        if 'leads_in' in query_params.keys():
            self.object_list = qs1
        elif 'follow_ups' in query_params.keys():
            self.object_list = qs2
        elif 'hot' in query_params.keys():
            self.object_list = qs.filter(
                hot=True, booked=False
            ).order_by('-modified').prefetch_related('customer', 'properties', 'leadproperty_set')
        elif 'booked' in query_params.keys():
            self.object_list = qs4
        else:
            self.object_list = QuerySetSequence(qs1, qs2, qs3, qs4)


        # Default is to allow empty querysets.  This can be altered by setting
        # `.allow_empty = False`, to raise 404 errors on empty querysets.
        if not self.allow_empty and not self.object_list:
            warnings.warn(
                'The `allow_empty` parameter is due to be deprecated. '
                'To use `allow_empty=False` style behavior, You should override '
                '`get_queryset()` and explicitly raise a 404 on empty querysets.',
                PendingDeprecationWarning
            )
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        # Switch between paginated or standard style responses
        page = self.paginate_queryset(self.object_list)
        db_time = time.time() - db_start
        serializer_start = time.time()
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)
        data = serializer.data
        serializer_time = time.time() - serializer_start
        return Response(data)


class MessageViewSet(NoCacheModelViewSet):
    """
    A simple ViewSet for viewing and editing messages.

    Filters:

    ?lead_id=40  can be filtered by lead_id
    """
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    filter_class = MessageFilterSet
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(MessageViewSet, self).get_queryset()
        user = CuserMiddleware.get_user()
        if user:
            if user.is_superuser:
                return qs.order_by('-processed')
            else:
                agency = get_agency()

                return qs.filter(mailbox=agency.mailbox).order_by('-processed')
        else:
            agency = get_agency()
            return qs.filter(mailbox=agency.mailbox).order_by('-processed')


class LeadPropertyListCreate(generics.ListCreateAPIView):
    model = LeadProperty
    serializer_class = serializers.LeadPropertySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        lead_pk = self.kwargs.get('lead_pk', None)
        if lead_pk is not None:
            user = CuserMiddleware.get_user()
            if user:
                if user.is_superuser:
                    return LeadProperty.objects.filter(lead__pk=lead_pk)
                else:
                    return LeadProperty.objects.filter(lead__pk=lead_pk, agency=get_agency())
            else:
                return LeadProperty.objects.filter(lead__pk=lead_pk, agency=get_agency())
        return []

    def pre_save(self, obj):
        lead_pk = self.kwargs.get('lead_pk', None)
        if lead_pk is not None:
            obj.lead_id = lead_pk
            return
        return Response(obj, status=status.HTTP_400_BAD_REQUEST)


class LeadPropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    model = LeadProperty
    serializer_class = serializers.LeadPropertySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(LeadPropertyDetail, self).get_queryset()
        user = CuserMiddleware.get_user()
        if user:
            if user.is_superuser:
                return qs
            else:
                return qs.filter(agency=get_agency())
        else:
            return qs.filter(agency=get_agency())


class LeadPropertyViewSet(NoCacheModelViewSet):
    """
    A simple ViewSet for viewing and editing properties.
    """
    model = LeadProperty
    serializer_class = serializers.LeadPropertySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        lead_pk = self.kwargs.get('lead_pk', None)
        if lead_pk is not None:
            user = CuserMiddleware.get_user()
            if user:
                if user.is_superuser:
                    return LeadProperty.objects.filter(lead__pk=lead_pk)
                else:
                    return LeadProperty.objects.filter(lead__pk=lead_pk, agency=get_agency())
            else:
                return LeadProperty.objects.filter(lead__pk=lead_pk, agency=get_agency())
        return []


class NotificationViewSet(NoCacheModelViewSet):
    model = Notification
    serializer_class = NotificationSerializer
    filter_class = NotificationFilterSet
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        qs = super(NotificationViewSet, self).get_queryset()
        user = CuserMiddleware.get_user()
        if user:
            if user.is_superuser:
                return qs
            else:
                return qs.filter(agency=get_agency())
        else:
            return qs.filter(agency=get_agency())


class NotificationLeadViewSet(NotificationViewSet):
    def get_queryset(self):
        qs = super(NotificationLeadViewSet, self).get_queryset()

        qs = qs.filter(
            Q(content_type=ContentType.objects.get_for_model(Message)) |
            Q(content_type=ContentType.objects.get_for_model(Lead)))
        return qs


class NoteViewSet(NoCacheModelViewSet):
    model = Note
    serializer_class = NoteSerializer
    filter_class = NoteFilterSet
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(NoteViewSet, self).get_queryset()
        user = CuserMiddleware.get_user()
        if user:
            if user.is_superuser:
                return qs
            else:
                return qs.filter(agency=get_agency())
        else:
            return qs.filter(agency=get_agency())

    def pre_save(self, obj):
        if not obj.user_id:
            obj.user = self.request.user

        return obj


class ReplyMessage(CreateAPIView):
    """
    Sends a message in response to the one passed as id in the url
    /api/reply/'id'/
    If the id is 0 means that has not been found any message to respond to.

    """
    serializer_class = ReplySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ReplySerializer(data=request.DATA)

        def record_send_message(email_msg, related_lead, sending_mailbox):
            """
            Records and sends a message with metadata for Mandrill.
            :param email_msg:
            :param related_lead:
            :param sending_mailbox:
            :return:
            """
            out_msg = sending_mailbox.record_outgoing_message(
                email.message_from_string(
                    email_msg.message().as_string()
                )
            )
            out_msg.lead = related_lead
            out_msg.save()
            email_msg = set_metadata(email_msg, out_msg)
            email_msg.send()
            return out_msg

        if serializer.is_valid():
            from fetchmyguest.utils.html2plaintext import html2plaintext
            import HTMLParser

            h = HTMLParser.HTMLParser()

            html_content = h.unescape(serializer.data['message'])
            text_content = html2plaintext(html_content, encoding='utf-8')

            if int(kwargs['msg_pk']) != 0:
                message = get_object_or_404(Message, pk=int(kwargs['msg_pk']))
                cc = []
                if serializer.data['cc']:
                    for address in serializer.data['cc'].split(','):
                        cc.append(
                            rfc822.parseaddr(
                                address
                            )[1]
                        )
                    # Forwarded message
                if serializer.data['fwd']:
                    to = []
                    for address in serializer.data['fwd'].split(','):
                        to.append(
                            rfc822.parseaddr(
                                address
                            )[1]
                        )

                    subject = 'Fwd: ' + message.subject

                    msg = EmailMessage(subject=subject, body=message.get_text_body(), to=to, cc=cc)
                    if message.mailbox.from_email:
                        msg.from_email = message.mailbox.from_email
                    else:
                        msg.from_email = settings.DEFAULT_FROM_EMAIL
                    record_send_message(msg, message.lead, message.mailbox)

                # Reply message
                else:
                    subject, to = 'Re: ' + ' '.join(message.subject.split()), message.lead.customer.email
                    msg = EmailMultiAlternatives(subject=subject, body=text_content, to=[to], cc=cc)
                    msg.attach_alternative(html_content, "text/html")
                    new_msg = message.prepare_reply(msg)
                    record_send_message(new_msg, message.lead, message.mailbox)
            else:
                lead = get_object_or_404(Lead, pk=int(kwargs['lead_pk']))
                if serializer.data['subject']:
                    subject = serializer.data['subject']
                else:
                    try:
                        lp = lead.leadproperty_set.filter(
                            Q(status=LeadProperty.REQUESTED) |
                            Q(status=LeadProperty.NOTAVAILABLE)
                        )[0]
                        subject = 'Property Request for {0}'.format(lp.property.title)
                    except:
                        subject = 'Property Request'

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    to=[lead.customer.email],
                    bcc=[lead.agency.email]
                )
                msg.attach_alternative(html_content, "text/html")
                record_send_message(msg, lead, lead.agency.mailbox)

            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class EmailResponseViewSet(ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Lead.objects.all()
    serializer_class = EmailResponseSerializer


class NoCacheRetrieveAPIView(RetrieveAPIView):

    @property
    def default_response_headers(self):

        return {
            'Allow': ', '.join(self.allowed_methods),
            'Vary': 'Accept',
            'Cache-Control': 'max-age=0, private, no-cache, no-store, must-revalidate, proxy-revalidate, no-transform'
        }

class FirstResponseTemplate(NoCacheRetrieveAPIView):
    serializer_class = FirstResponseTemplateSerializer
    model = Lead

    def get_object(self, queryset=None):
        pk = self.kwargs.get('lead_pk', None)
        obj = Lead.objects.get(pk=pk)
        return obj


class SecondResponseTemplate(NoCacheRetrieveAPIView):
    serializer_class = SecondResponseTemplateSerializer
    model = Lead

    def get_object(self, queryset=None):
        pk = self.kwargs.get('lead_pk', None)
        obj = Lead.objects.get(pk=pk)
        return obj


class OfferResponseTemplate(NoCacheRetrieveAPIView):
    serializer_class = OfferResponseTemplateSerializer
    model = Lead

    def get_object(self, queryset=None):
        pk = self.kwargs.get('lead_pk', None)
        obj = Lead.objects.get(pk=pk)
        return obj


class ConciergeResponseTemplate(NoCacheRetrieveAPIView):
    serializer_class = ConciergeResponseTemplateSerializer
    model = Lead

    def get_object(self, queryset=None):
        pk = self.kwargs.get('lead_pk', None)
        obj = Lead.objects.get(pk=pk)
        return obj


class DefaultResponseTemplate(NoCacheRetrieveAPIView):
    serializer_class = DefaultResponseTemplateSerializer
    model = Lead

    def get_object(self, queryset=None):
        pk = self.kwargs.get('lead_pk', None)
        obj = Lead.objects.get(pk=pk)
        return obj

if settings.DEBUG:
    def start(sender, **kwargs):
        global started
        started = time.time()

    def finish(sender, **kwargs):
        total = time.time() - started
        api_view_time = dispatch_time - (render_time + serializer_time + db_time)
        request_response_time = total - dispatch_time

        logger.debug("Database lookup               | %.4fs" % db_time)
        logger.debug("Serialization                 | %.4fs" % serializer_time)
        logger.debug("Django request/response       | %.4fs" % request_response_time)
        logger.debug("API view                      | %.4fs" % api_view_time)
        logger.debug("Response rendering            | %.4fs" % render_time)

    request_started.connect(start)
    request_finished.connect(finish)