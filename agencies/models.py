from __future__ import unicode_literals
from cuser.middleware import CuserMiddleware
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django_localflavor_us.models import PhoneNumberField
from django.conf import settings
from fetchmyguest.utils.models import has_changed
from django_hstore.hstore import HStoreManager


####################### CONSTANTS ##############################
# Here we define the fields names to avoid repetitions and errors
# We'll never refer to a model field directly, always use a constant
# defined here, this improves
SOURCE = 'source_id'
SUBJECT = 'subject'

LEAD_QUALIFIERS = [
    SOURCE,
    SUBJECT
]
LEAD_QUALIFIERS_DESC = [
    '**Source Identifier',
    '**Lead Subject Qualifier'
                       ]

PROPERTIES = 'properties'
ARRIVAL = 'arrival'
DEPARTURE = 'departure'
ADULTS = 'adults'
CHILDREN = 'children'

LEAD_FIELDS = [
    PROPERTIES,
    ARRIVAL,
    DEPARTURE,
    ADULTS,
    CHILDREN,
    ]

LEAD_FIELDS_DESC = [
    'Property ID',
    'Arrival',
    'Departure',
    'Adults',
    'Children',
    ]

FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
PHONE = 'phone'
EMAIL = 'email'

####################### Customer Model ##############################

CUSTOMER_FIELDS = [
    FIRST_NAME,
    LAST_NAME,
    PHONE,
    EMAIL,
    ]

CUSTOMER_FIELDS_DESC = [
    'Customer First name',
    'Customer Last name',
    'Customer Phone',
    'Customer email',
    ]

TARGET_FIELDS = zip(LEAD_QUALIFIERS, LEAD_QUALIFIERS_DESC) + zip(CUSTOMER_FIELDS, CUSTOMER_FIELDS_DESC) \
                    + zip(LEAD_FIELDS, LEAD_FIELDS_DESC)

####################### Message Model ##############################
EMAIL_FIELDS = ['body',
                'from_header',
                'in_reply_to',
                'message_id',
                'replies',
                'subject',
                'to_header']

MESSAGE_FIELDS = zip(EMAIL_FIELDS, EMAIL_FIELDS)




####################### END CONSTANTS ##############################


def get_agency(user=None):
    from agencies.models import Agency
    if not user:
        user = CuserMiddleware.get_user()
    try:
        agency = user.agent_profile.agency
    except:
        agency = Agency.objects.get(id=settings.DEFAULT_AGENCY_ID)
    return agency

class AgencyIsolatedManager(models.Manager):

    def get_query_set(self):
        qs = super(AgencyIsolatedManager, self).get_query_set()
        user = CuserMiddleware.get_user()
        if user:
            if user.is_superuser:
                return qs
            else:
                return qs.filter(agency=get_agency())
        else:
            return qs.filter(agency=get_agency())


class AgencyIsolatedHstoreManager(HStoreManager):

    def get_query_set(self):
        qs = super(AgencyIsolatedHstoreManager, self).get_query_set()
        user = CuserMiddleware.get_user()
        if user:
            if user.is_superuser:
                return qs
            else:
                return qs.filter(agency=get_agency())
        else:
            return qs.filter(agency=get_agency())

class AgencyIsolatedModel(models.Model):
    agency = models.ForeignKey('Agency', null=True)

    objects = AgencyIsolatedManager()

    class Meta:
        abstract = True

class AgencyIsolatedHstoreModel(models.Model):
    agency = models.ForeignKey('Agency', null=True)

    objects = AgencyIsolatedHstoreManager()

    class Meta:
        abstract = True



class LeadSource(models.Model):
    name = models.CharField(max_length=50)
    agency = models.ForeignKey('Agency', related_name='sources')
    priority = models.IntegerField(choices=zip(range(6), range(6)), default=0)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['priority',]

class RegexRule(models.Model):
    """
    Regular expressions
    Examples:
    Customer email
    (?:Reply-To:(?: )*)[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?

    Customer name and Surname
    (?:Guest Name:(?: )*)(\w*(?: )*)+

    Departure date:
    (?<= - )(?<departure>\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|[0-9]|1[0-2])(?:\s|\.|-)(?:\d|[0-2][0-9]|3[0-1])(?:st|rd|nd)?,?(?:\s|\.|-)\b\d{1,4}\b)

    Customer email:
    (?<=Email )(?<email>[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9]))*

    Remember to use specify the correct matching group

    """
    source = models.ForeignKey(LeadSource, related_name='rules', null=True)
    matching_group_name = models.CharField(max_length=50)
    field = models.CharField(max_length=50, choices=MESSAGE_FIELDS, default='body', verbose_name='Email field')
    target_field = models.CharField(max_length=50, choices=TARGET_FIELDS, default='source_id')
    regex = models.TextField()
    example_text = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '{0} - {1}'.format(self.source, self.matching_group_name)

    def save(self, **kwargs):
        """
        When it is saved a new Rule we update the cache
        :param kwargs:
        :return:
        """
        from fetchmyguest.utils.parse_email import update_rules_cache
        obj = super(RegexRule, self).save(**kwargs)
        update_rules_cache()
        return obj


class Agency(models.Model):
    """
    Defines an agency as group of agents
    """
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', null=True, blank=True)
    state = models.ForeignKey('cities_light.Region', null=True, blank=True)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True, null=True)
    fax = PhoneNumberField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    mailbox = models.ForeignKey('django_mailbox.Mailbox', null=False)
    smtp_host = models.CharField(max_length=255, blank=True, default='')
    smtp_port = models.IntegerField(default=0)
    smtp_user = models.CharField(max_length=255, blank=True, default='')
    smtp_password = models.CharField(max_length=255, blank=True, default='')
    smtp_use_tls = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0} - {1}'.format(self.name, self.email)

    class Meta:
        verbose_name_plural = "Agencies"


class Agent(models.Model):
    """
    UserRena Profile to allow registration and email verification
    """
    agency = models.ForeignKey(Agency, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                unique=True,
                                verbose_name='user',
                                related_name='agent_profile')
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', null=True, blank=True)
    state = models.ForeignKey('cities_light.Region', null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    email_signature = models.TextField(null=True, blank=True)

    objects = AgencyIsolatedManager()

    def __unicode__(self):
        return self.user


class EmailTemplate(models.Model):
    """
    Templates that will be used when sending emails
    """
    agency = models.OneToOneField(Agency, editable=False)
    name = models.CharField(max_length=40)
    html_template = models.TextField()

    objects = AgencyIsolatedManager()

    def __unicode__(self):
        return self.name

class SecondEmailTemplate(models.Model):
    """
    Templates that will be used when sending emails
    """
    agency = models.OneToOneField(Agency, editable=False)
    name = models.CharField(max_length=40)
    html_template = models.TextField()

    objects = AgencyIsolatedManager()

    def __unicode__(self):
        return self.name

# class SecondEmailTemplate(models.Model):
#     """
#     Templates that will be used when sending emails
#     """
#     agency = models.OneToOneField(Agency, editable=False)
#     name = models.CharField(max_length=40)
#     html_template = models.TextField()
#
#     def __unicode__(self):
#         return self.name

class SpecialOfferTemplate(models.Model):
    """
    Templates that will be used when sending emails
    """
    agency = models.ForeignKey(Agency, editable=False)
    name = models.CharField(max_length=40)
    start = models.DateField(default=timezone.now().date(), editable=True)
    end = models.DateField(default=timezone.now().date(), editable=True)
    html_template = models.TextField()

    objects = AgencyIsolatedManager()

    def __unicode__(self):
        return self.name


class ConciergeTemplate(models.Model):
    """
    Templates that will be used when sending emails
    """
    agency = models.OneToOneField(Agency, editable=False)
    name = models.CharField(max_length=40)
    html_template = models.TextField()

    objects = AgencyIsolatedManager()

    def __unicode__(self):
        return self.name



class Notification(AgencyIsolatedModel):
    """
    Notifications are the messages popped up to users
    they contain reference to the object
    Defining a permalink decorator we can add a popup to display that
    object:
    from django.db.models import *

    class Something(Model):
        slug = CharField(max_length=50)
        title = CharField(max_length=100)
        text = TextField(blank=True)

        @permalink
        def get_absolute_url(self):
            return ('views.view_something', (), {'slug': self.slug})
        @permalink
        def get_edit_url(self):
            return ('views.view_something_edit', (), {'slug': self.slug})
        @permalink
        def get_json_url(self):
            return ('views.view_something_json', (), {'slug': self.slug})
        @permalink
        def get_html_chunk_url(self):
            return ('views.view_something_ajax', (), {'slug': self.slug})

    <h1>{{ notification.content_object }}</h1>
    <ul>
    <li><a href="{{ notification.content_object.get_absolute_url }}">View</a></li>
    <li><a href="{{ notification.content_object.get_edit_url }}">Edit</a></li>
    </ul>
    OR
    $.getJSON('{{ notification.content_object.get_json_url }}', function(something) {
        // The variable 'something' now received your data
    });
    OR
    $('#something').load('{{ notification.content_object.get_html_chunk_url }}');


    """

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    content = models.TextField(default='')
    alert = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    viewed_on = models.DateTimeField(null=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if has_changed(self, 'viewed') and self.viewed:
            self.viewed_on = timezone.now()
        if not self.agency:
            self.agency = get_agency()
        if self.alert:  # Not saving Notifications that don't create an alert
            super(Notification, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.content[:50]








