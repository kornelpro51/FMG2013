from __future__ import unicode_literals
import email
import json
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
from django.db import models
from django.forms import widgets
from django.utils import timezone
import re
from rest_framework.reverse import reverse
from agencies.models import Notification
from django_mailbox.models import Message
from rest_framework import serializers, pagination
from django.template.loader import get_template_from_string
from django.template.context import Context
from events_logger.models import LogEvents

from leads.models import Customer, Lead, LeadProperty, Note, Property

class CustomHyperlinkedField(serializers.HyperlinkedRelatedField):

    def field_to_native(self, obj, field_name):
        return reverse(self.view_name, kwargs={'lead_pk': obj.id}, request=self.context['request'])

    def get_url(self, obj, view_name, request, format):
        kwargs = {'lead_pk': obj.id}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)



class HstoreField(serializers.Field):

    def to_native(self, value):
        out = dict()
        for k, v in value.iteritems():
            try:
                v = LogEvents.from_json(v).to_dict() or json.loads(v)
            except:
                pass
            out.update({k: v})
        return out

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    # leads = serializers.PrimaryKeyRelatedField(many=True, )
    first_name = serializers.CharField(required=False)

    def perform_validation(self, attrs):
        if not attrs.get('first_name'):
            if attrs.get('email'):
                attrs['first_name'] = attrs['email']
                self.data['first_name'] = attrs['email']
            else:
                raise serializers.ValidationError('Invalid data')

        attrs = super(CustomerSerializer, self).perform_validation(attrs)
        return attrs

    def from_native(self, data, files):
        instance = super(CustomerSerializer, self).from_native(data, files)
        return instance

    def save(self, **kwargs):
        try:
            self.object = super(CustomerSerializer, self).save(**kwargs)
            return self.object
        except ValidationError as e:
            try:
                self.object = Customer.objects.get(agency=self.object.agency, email__iexact=self.object.email)
                return self.object
            except ObjectDoesNotExist:
                raise serializers.ValidationError(repr(e))
            except MultipleObjectsReturned:
                self.object = Customer.objects.filter(agency=self.object.agency, email__iexact=self.object.email)[0]
                return self.object


    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone']

class PlainMessageSerializer(serializers.Field):
    def field_from_native(self, data, files, field_name, into):
        pass

    def field_to_native(self, obj, field_name):
        if field_name != 'abstract':
            return obj.get_text_body()
        else:
            text = obj.get_text_body()
            abstract = text.replace('\r\n\r\n', ' ').replace('\r\n', ' ').replace('\t', ' ').replace('  ', ' ')
            return abstract[:80]

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(source='lead', many=False)
    user = serializers.Field(source='user.email')
    class Meta:
        model = Note
        fields = [
            'id',
            'url',
            'lead',
            'user',
            'content',
            'created',
            'modified'
        ]


class CustomDecimal(serializers.DecimalField):

    def to_native(self, value):
        return '{0:.2f}'.format(value).rstrip('0').rstrip('.')


class PropertySerializer(serializers.HyperlinkedModelSerializer):
    city = serializers.CharField(source='city.name')
    state = serializers.CharField(source='state.name')
    bathrooms = CustomDecimal()
    class Meta:
        model = Property
        fields = ['id',
                  'url',
                  'title',
                  'address',
                  'city',
                  'state',
                  'description',
                  'sleeps',
                  'bathrooms',
                  'bedrooms',
                  'loft',
                  'link',
                  'rate',
                  ]


class LeadPropertySerializer(serializers.HyperlinkedModelSerializer):
    available_from = serializers.DateField(format='iso-8601', required=False)
    available_to = serializers.DateField(format='iso-8601', required=False)
    property = serializers.PrimaryKeyRelatedField(source='property', many=False)
    property_details = PropertySerializer(source='property', read_only=True)
    lead = serializers.Field(source='lead.id')
    class Meta:
        model = LeadProperty
        fields = ['id',
                  'url',
                  'available_from',
                  'available_to',
                  'lead',
                  'property',
                  'property_details',
                  'rate',
                  'status',
                  'order']

class MessageSerializer(serializers.ModelSerializer):
    in_reply_to = serializers.PrimaryKeyRelatedField(source='in_reply_to', many=False)
    lead = serializers.PrimaryKeyRelatedField(source='lead', many=False)
    body = PlainMessageSerializer()
    events = HstoreField(source='events')
    class Meta:
        model = Message
        exclude = [
            'mailbox',
        ]

class LeadSerializer(serializers.HyperlinkedModelSerializer):

    def get_reply_id(self, obj):
        m = first(obj.messages.filter(outgoing=False).order_by('-processed'))
        if not m:
            return 0
        return m.pk

    def get_reply_url(self, obj):

        return reverse(viewname='reply-message', kwargs={'lead_pk': obj.id, 'msg_pk': self.get_reply_id(obj)}, request=self.context['request'])


    modified = serializers.DateTimeField(format='iso-8601', required=False, read_only=True)
    arrival = serializers.DateField(format='iso-8601', required=False)
    departure = serializers.DateField(format='iso-8601', required=False)
    customer_serial = CustomerSerializer(source='customer', many=False, read_only=True)
    customer = serializers.PrimaryKeyRelatedField(source='customer', many=False)
    customer_name = serializers.Field(source='customer')
    lead_properties = LeadPropertySerializer(source='leadproperty_set', read_only=True)
    reply_message_url = serializers.SerializerMethodField('get_reply_url')


    # properties = LeadPropertySerializer(source='leadproperty_set', many=True)
    class Meta:
        model = Lead
        fields = ['id',
                  'url',
                  'created',
                  'modified',
                  'arrival',
                  'departure',
                  'source',
                  'customer',
                  'customer_serial',
                  'customer_name',
                  'adults',
                  'children',
                  'phone_call',
                  'first_response',
                  'second_response',
                  'offer',
                  'hot',
                  'long_term',
                  'booked',
                  'booked_date',
                  # 'messages',
                  # 'events',
                  # 'notes',
                  'lead_properties',
                  'reply_message_url',
                  ]





class NotificationRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_native(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Message):
            return LeadSerializer(instance=value.lead, context={'request': None}).data
        elif isinstance(value, Lead):
            return LeadSerializer(instance=value, context={'request': None}).data
        elif isinstance(value, Property):
            return dict(type='property', id=str(value.pk))
        raise Exception('Unexpected type of tagged object')


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    object = NotificationRelatedField(source='content_object')
    class Meta:
        model = Notification
        fields = ['content',
                  'created',
                  'object',
                  'id',
                  'alert',
                  'modified',
                  'viewed',
                  'viewed_on']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

class ReplySerializer(serializers.Serializer):

    fwd = serializers.CharField(max_length=255, required=False)

    cc = serializers.CharField(max_length=255, required=False)

    subject = serializers.CharField(widget=widgets.Textarea,
                                 max_length=100000, default='', required=False)
    message = serializers.CharField(widget=widgets.Textarea,
                                 max_length=100000, required=False)

def first(query):
    try:
        return query.all()[0]
    except:
        return None


class TemplateSerializer(serializers.Field):

    def field_to_native(self, obj, field_name):
        t = get_template_from_string('No template found')
        agency = None
        agent = None
        try:
            agency = self.context['view'].request.user.agent_profile.agency
            agent = self.context['view'].request.user.agent_profile
            if field_name == 'first_response':
                t = get_template_from_string(agency.emailtemplate.html_template)
            if field_name == 'second_response':
                t = get_template_from_string(agency.secondemailtemplate.html_template)
            if field_name == 'offer_response':
                TODAY = timezone.now().date()
                template = first(agency.specialoffertemplate_set.filter(start__lte=TODAY, end__gte=TODAY))
                t = get_template_from_string(template.html_template)
            if field_name == 'concierge_response':
                t = get_template_from_string(agency.conciergetemplate.html_template)
            if field_name == 'default_response':
                t = get_template_from_string(agent.email_signature)
        except Exception as e:
            t = get_template_from_string('{0}'.format(repr(e)))
        context = Context(
            dict(
                requested_properties=obj.leadproperty_set.filter(status=LeadProperty.REQUESTED),
                not_available_properties=obj.leadproperty_set.filter(status=LeadProperty.NOTAVAILABLE),
                proposed_properties=obj.leadproperty_set.filter(status=LeadProperty.PROPOSED),
                lead=obj,
                agent=agent,
                agency=agency
                )
        )
        rendered = t.render(context)
        return rendered

class BodySerializer(serializers.WritableField):
    def field_to_native(self, obj, field_name):
        body = obj.get_text_body()
        return body
    def field_from_native(self, data, files, field_name, into):
        body = data
        return body

class ToHeaderSerializer(serializers.WritableField):

    def field_from_native(self, data, files, field_name, into):
        recievers = re.findall(r"(\b[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}\b)", data)
        return recievers

class ForwardSerializer(serializers.ModelSerializer):
    to_header = ToHeaderSerializer()
    body = BodySerializer()
    class Meta:
        model = Message
        exclude = [
            'message_id',
            'in_reply_to',
            'from_header',
            'outgoing',
            'read',
            'lead',
            'is_lead_source',
            'mailbox',
        ]

class EmailResponseSerializer(serializers.Serializer):
    first_response = CustomHyperlinkedField(source='id', view_name='lead-first_response',  many=False, read_only=True)
    second_response = CustomHyperlinkedField(source='id', view_name='lead-second_response',  many=False, read_only=True)
    offer_response = CustomHyperlinkedField(source='id', view_name='lead-offer_response',  many=False, read_only=True)
    concierge_response = CustomHyperlinkedField(source='id', view_name='lead-concierge_response',  many=False, read_only=True)
    default_response = CustomHyperlinkedField(source='id', view_name='default_response',  many=False, read_only=True)

class FirstResponseTemplateSerializer(serializers.Serializer):
    first_response = TemplateSerializer()

class SecondResponseTemplateSerializer(serializers.Serializer):
    second_response = TemplateSerializer()

class OfferResponseTemplateSerializer(serializers.Serializer):
    offer_response = TemplateSerializer()

class ConciergeResponseTemplateSerializer(serializers.Serializer):
    concierge_response = TemplateSerializer()

class DefaultResponseTemplateSerializer(serializers.Serializer):
    default_response = TemplateSerializer()
