from __future__ import unicode_literals
from braces.views import JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View
from django_mailbox.models import Message
from rest_framework import generics, permissions
from rest_framework.renderers import JSONRenderer

from leads.models import Customer, Lead, Note, Property
from leads.serializers import (
    CustomerSerializer,
    LeadSerializer,
    MessageSerializer,
    NoteSerializer,
    PropertySerializer,
    UserSerializer,
)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)




class LeadJsonView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):
    def get(self, request, *args, **kwargs):
        return self.render_json_object_response(Lead.objects.all())


class LeadJsonViewRest(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        leadsserializer = LeadSerializer(Lead.objects.all(), many=True)
        json_data = leadsserializer.data
        return JSONResponse(json_data)


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = None


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PropertyList(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = None


class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = (permissions.IsAuthenticated,)


class LeadListForCurrentMonth(generics.ListCreateAPIView):
    queryset = Lead.objects.filter(
        created__year=datetime.now().strftime('%Y'),
        created__month=datetime.now().strftime('%m')
    ).order_by('-created')
    serializer_class = LeadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = None


class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NoteListForLead(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = None

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        try:
            lead = Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            lead = None

        queryset = Note.objects.filter(lead=lead)

        return queryset

    def pre_save(self, obj):
        pk = self.kwargs.get('pk', None)
        try:
            lead = Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            lead = None
        obj.lead = lead
        obj.user = self.request.user


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)




class MessageListForLead(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = None

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        try:
            lead = Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            lead = None

        queryset = Message.objects.filter(lead=lead)

        return queryset


class MessageDetail(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)


