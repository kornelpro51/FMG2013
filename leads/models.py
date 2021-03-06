from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django_hstore.hstore import DictionaryField
from django_localflavor_us.models import PhoneNumberField
from django_mailbox.models import Message
from djrill.signals import webhook_event
from agencies.models import AgencyIsolatedModel, get_agency, AgencyIsolatedHstoreModel, AgencyIsolatedHstoreManager, AgencyIsolatedManager
from django.conf import settings
from django.db.models.base import ValidationError
from django_mailbox.signals import message_received
from fetchmyguest.utils.django_mailbox import prepare_reply, get_text_body
from fetchmyguest.utils.parse_email import check_email_for_lead
from leads.webhook_handlers import handle_mandrill

####################### CONSTANTS ##############################
# Here we define the fields names to avoid repetitions and errors
# We'll never refer to a model field directly, always use a constant
# defined here, this improves
####################### Lead Model ##############################
BATH = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]
BATH_DATA = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]
BATH_CHOICES = zip(BATH_DATA, BATH)
BED_CHOICES = zip(range(9), range(9))
SLEEP_CHOICES = zip(range(17), range(17))




class Customer(AgencyIsolatedModel):
    """
    Customers are generated by the same process that creates the Lead, if their email is matched are simply linked.
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = AgencyIsolatedManager()

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def save(self, **kwargs):
        """
        When it is saved a new Customer we update the cache
        :param kwargs:
        :return:
        """
        from fetchmyguest.utils.parse_email import update_customers_cache

        if not self.agency:
            self.agency = get_agency()
        if not self.first_name:
            if self.email:
                self.first_name = self.email
            else:
                raise ValidationError('Missing Field, either first_name or email')

        if (self.email and not Customer.objects.filter(agency=self.agency, email__iexact=self.email).exists()) \
            or not self.email \
            or self.id:
            self.email = self.email.lower()
            super(Customer, self).save(**kwargs)
            update_customers_cache()
        else:
            raise ValidationError('Cannot save a email address twice')


class Property(AgencyIsolatedHstoreModel):
    """
    For now are imported, than can be originated from parsing, eventually can generated when not matched.
    """
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    city = models.ForeignKey('cities_light.City', null=True, blank=True)
    state = models.ForeignKey('cities_light.Region', null=True, blank=True)
    property_ids = DictionaryField(db_index=True, verbose_name="Source Property IDS", default={"": ""})
    bathrooms = models.DecimalField(choices=BATH_CHOICES, decimal_places=1, max_digits=2, default=0)
    bedrooms = models.IntegerField(default=0, choices=BED_CHOICES)
    loft = models.BooleanField(default=False)
    sleeps = models.IntegerField(default=0, choices=SLEEP_CHOICES)
    description = models.TextField(blank=True, verbose_name="Description", default='')
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    link = models.URLField(null=True, blank=True, verbose_name="Property Link")
    book = models.URLField(null=True, blank=True, verbose_name="Book Me Link")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    approved = models.NullBooleanField(default=False)

    objects = AgencyIsolatedHstoreManager()

    def save(self, **kwargs):

        if not self.agency:
            self.agency = get_agency()
        if not self.property_ids:
            self.property_ids = {}
        else:
            lower_dict = {}
            for k, v in self.property_ids.iteritems():
                lower_dict[k.lower().strip()] = v.lower().strip()
            self.property_ids = lower_dict
        obj = super(Property, self).save(**kwargs)
        return obj


    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['address']


class LeadProperty(AgencyIsolatedModel):
    """
    Properties related to a lead with the status  to define the way they relate
    """
    REQUESTED = 'RQ'
    PROPOSED = 'PR'
    NOTAVAILABLE = 'NA'
    NOTACCEPTED = 'PN'
    BOOKED = 'BO'

    STATUS_CHOICES = (
        (REQUESTED, 'Requested by Customer'),
        (PROPOSED, 'Proposed'),
        (NOTAVAILABLE, 'Requested but not available'),
        (NOTACCEPTED, 'Proposed but not accepted'),
        (BOOKED, 'Booked'),
    )

    lead = models.ForeignKey('Lead')
    property = models.ForeignKey(Property, related_name='leads')
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    suggested_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PROPOSED)
    order = models.IntegerField(default=0)

    objects = AgencyIsolatedManager()

    def save(self, **kwargs):
        if not self.agency:
            self.agency = get_agency()
        obj = super(LeadProperty, self).save(**kwargs)

        return obj

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "property__name__icontains",)

    def __unicode__(self):
        return '{0} - {1}'.format(self.property, self.lead)

    class Meta:
        verbose_name_plural = "LeadProperties"
        ordering = ['order', '-id']


class Lead(AgencyIsolatedHstoreModel):
    """
    Lead are generated when a new email is saved and the Regular Expression Rules related to the registered
    agencies are matched, this triggers the email content extraction and the lead generation when the email
    has not an 'In-Reply', in this case the message is queued to the matching lead
    """
    customer = models.ForeignKey(Customer, related_name='leads')
    properties = models.ManyToManyField(Property, through=LeadProperty, null=True)
    source = models.CharField(max_length=255)
    arrival = models.DateField(null=True, blank=True)
    departure = models.DateField(null=True, blank=True)
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    phone_call = models.BooleanField(default=False)
    first_response = models.BooleanField(default=False)
    second_response = models.BooleanField(default=False)
    offer = models.BooleanField(default=False)
    hot = models.BooleanField(default=False)
    long_term = models.BooleanField(default=False)
    booked = models.BooleanField(default=False)
    booked_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    events = DictionaryField(verbose_name="Events log", default={"": ""})

    objects = AgencyIsolatedHstoreManager()

    def lead_properties(self):
        return self.properties.all()

    def save(self, **kwargs):

        if not self.agency:
            self.agency = get_agency()

        if self.booked:  # When a Lead is booked cannot be hot anymore
            self.hot = False
            if not self.booked_date:
                self.booked_date = timezone.now()
        obj = super(Lead, self).save(**kwargs)
        return obj

    def __unicode__(self):
        return '{0} - {1}'.format(self.customer, self.created.date())

    class Meta:
        ordering = ['-created', '-hot', '-modified']


class Note(AgencyIsolatedModel):
    """
    Permits to add reference notes
    """

    lead = models.ForeignKey(Lead, related_name='notes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = AgencyIsolatedManager()

    def save(self, **kwargs):
        from fetchmyguest.utils.notifications import notify

        if not self.agency:
            self.agency = get_agency()
        obj = super(Note, self).save(**kwargs)
        #from fetchmyguest.utils.notifications import notify
        notify(self.lead, 'Note for lead: {0}'.format(self.lead.customer), alert=True)
        return obj

    def __unicode__(self):
        return self.content[:50]
Message.add_to_class('lead', models.ForeignKey(Lead, related_name='messages', null=True, blank=True))
Message.add_to_class('is_lead_source', models.NullBooleanField())
Message.add_to_class('events', DictionaryField(verbose_name="Events log", default={"": ""}))
Message.add_to_class('prepare_reply', prepare_reply)
Message.add_to_class('get_text_body', get_text_body)
# Message.objects = HStoreManager()
message_received.connect(check_email_for_lead)
webhook_event.connect(handle_mandrill)