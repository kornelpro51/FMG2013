from __future__ import unicode_literals
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from leads.models import Lead

class LeadResource(ModelResource):
    class Meta:
        queryset = Lead.objects.all()
        resource_name = 'lead'
        authorization = Authorization()
