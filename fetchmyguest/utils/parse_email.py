from __future__ import unicode_literals

from django.utils import timezone
from fetchmyguest.utils.email_utils import get_valid_email

from fetchmyguest.utils.notifications import notify
from fetchmyguest.utils.numbers import int_or_0

from agencies.models import PHONE, FIRST_NAME, LAST_NAME, EMAIL, ARRIVAL, DEPARTURE, ADULTS, CHILDREN, SOURCE, SUBJECT, PROPERTIES
import re
from django.core.cache import cache
from dateutil.parser import parse as date_parse
from dateutil.relativedelta import relativedelta

import logging

logger = logging.getLogger('')

from django.conf import settings

CACHING_ENABLED = getattr(settings, 'QUERY_CACHING_ENABLED', True)
CACHE_TIMEOUT = getattr(settings, 'LEAD_GENERATION_CACHING_TIMEOUT', 300)


def match_rule(msg, rule):
    """
    Function to match regex rules
    
    Keyword arguments:
    :param msg      a django mailbox Message object
    :param rule     a RegexRule object

    :return string   returns the matching string or ''
    """
    result = ''
    try:
        regex = re.compile(rule.regex)
        if rule.field == 'body':
            message_content = msg.get_text_body()
        else:
            message_content = getattr(msg, rule.field, None)
        logger.debug('Matching {0}\n group: {1}\n email_field: {2}'.format(rule.regex,
                                                                           rule.matching_group_name,
                                                                           rule.field,
        ))
        m = regex.search(message_content)
        if m:
            result = m.group(rule.matching_group_name)
    except Exception as e:
        logger.error('Error matching a rule: {0}'.format(str(e)))
    finally:
        logger.debug('Regex result:\n{0}'.format(result))
        return result.strip()


def get_rules(source, target_field):
    """
    Function to match regex rules

    Keyword arguments:
    :param source       object    a lead source model object
    :param target_field string    a target field name

    :return queryset  returns a cached queryset
    """
    try:
        key = 'rules_{0}_{1}'.format(source.name, target_field)
        if CACHING_ENABLED:
            rules = cache.get(key)
            if not rules:
                rules = source.rules.filter(target_field=target_field)
                cache.set(key, rules, CACHE_TIMEOUT)
            return rules
        else:
            rules = source.rules.filter(target_field=target_field)
        return rules
    except Exception:
        return []

def update_rules_cache():
    """
    Clears the rules cache, so we can set a long timeout

    :return:
    """
    if CACHING_ENABLED:
        from agencies.models import RegexRule, LeadSource
        target_fields = RegexRule.objects.values_list('target_field').distinct()
        for target_field in target_fields:
            for source in LeadSource.objects.filter(active=True):
                rules = source.rules.filter(target_field=target_field[0])
                key = 'rules_{0}_{1}'.format(source.name, target_field[0])
                cache.set(key, rules, CACHE_TIMEOUT)
    return


def apply_rules(source, msg, target_field):
    """
    Function to match all the rules and obtain a single value
    the first match end the process.

    Keyword arguments:
    :param source       object    a lead source model object
    :param msg      a django mailbox Message object
    :param target_field string    a target field name

    """
    result = ''
    for rule in get_rules(source, target_field=target_field):  # We can have more rules to match to identify a source
        match_value = match_rule(msg, rule)
        if match_value:
            result = match_value
            return result
    return result


def get_property(property_id, source):
    """

    :param property_id:
    :param source:
    :return:
    """
    from leads.models import Property
    p_id = property_id.lower()
    s_name = source.name.lower()
    obj, created = None, False
    try:
        obj = Property.objects.filter(property_ids__contains=({s_name: p_id}))[0]
    except IndexError:
        try:
            obj = Property(
                title='{0} property : {1}'.format(source.name, property_id),
                agency=source.agency,
                property_ids={s_name: p_id},
            )
            obj.save()
            created = True
        except Exception as e:
            logger.error('Error:{0} creating a property with ID: {0} for {1} '.format(str(e)), property_id, source.name)
            return None, False
    except Exception as e:
        logger.error('Error:{0} searching the property with ID: {0} for {1} '.format(str(e)), property_id, source.name)
        return None, False
    if created:
        content = 'New {0} property'.format(source.name)
        notify(obj, content)
    return obj, created


def get_or_create_customer(source, msg):
    """

    :param source:
    :param msg:
    :return:
    """
    obj = None
    from leads.models import Customer
    c_email = apply_rules(source, msg, EMAIL)
    c_first_name = apply_rules(source, msg, FIRST_NAME)
    try:
        if c_email:
            if not Customer.objects.filter(agency=source.agency, email__iexact=c_email).exists():
                obj = Customer(
                    agency=source.agency,
                    first_name = c_first_name,
                    last_name = apply_rules(source, msg, LAST_NAME),
                    email = c_email.lower(),
                    phone = apply_rules(source, msg, PHONE)
                )
                obj.save()
            else:
                obj = Customer.objects.filter(agency=source.agency, email__iexact=c_email)[0]
        elif c_first_name:
                obj = Customer(
                    agency=source.agency,
                    first_name = c_first_name,
                    last_name = apply_rules(source, msg, LAST_NAME),
                    email = c_email.lower(),
                    phone = apply_rules(source, msg, PHONE)
                )
                obj.save()
    except Exception as e:
        logger.error('Cannot create a customer, Error: '.format(repr(e)))
    return obj


def create_lead(source=None, msg=None, customer=None):
    """
    Main function generate leads

    Keyword arguments
    :param source   object      a LeadSource object
    :param msg      object      a django mailbox Message object
    :param customer object

    :return None  nothing to return
    """
    from leads.models import Lead, LeadProperty
    property = None
    lead, lead_created = None, False

    TODAY = timezone.now().date()
    try:
        CUT_OFF_DAYS = settings.LEADS_CUT_OFF_DAYS
    except:
        CUT_OFF_DAYS = 30

    CUT_OFF_DATE = TODAY + relativedelta(days=-CUT_OFF_DAYS)

    ######################## Check for a property using the id in the message ###################
    if source:
        property_id = apply_rules(source, msg, target_field=PROPERTIES)
        if property_id:
            property, property_created = get_property(property_id=property_id, source=source)

        else:
            logger.warning('No property id found in message ID:{0}, source: {1}'.format(msg.id, source.name))

        if not customer:
            customer = get_or_create_customer(source, msg)

        msg_arrival=date_parse(apply_rules(source, msg, target_field=ARRIVAL)).date() or TODAY
        msg_departure=date_parse(apply_rules(source, msg, target_field=DEPARTURE)).date() or TODAY
        msg_adults=int_or_0(apply_rules(source, msg, target_field=ADULTS))
        msg_children=int_or_0(apply_rules(source, msg, target_field=CHILDREN))
        agency = source.agency
        source_name = source.name

    elif customer:
        agency = customer.agency
        source_name = 'Customer message'
        msg_arrival = msg_departure = TODAY
        msg_adults = msg_children = 0
    else:  # Cannot create a lead with no source and no customer
        logger.error('Message id: {0} Cannot create a lead with no source and no customer'.format(msg.id))
        return '', False

    ############################ We have all we need to create or get a lead ##############################
    try:
        lead = Lead.objects.filter(customer=customer,
                                   agency=agency,
                                   # This line below will allow to aggregate leads from the same source
                                   # source__iexact=source_name,
                                   created__gt=CUT_OFF_DATE,
                                   booked=False).order_by('-modified')[0]
    except (IndexError, Lead.DoesNotExist):
        # No leads found, let's create one
        try:
            lead = Lead(
                customer=customer,
                arrival=msg_arrival,
                departure=msg_departure,
                adults=msg_adults,
                children=msg_children,
                source=source_name,
                agency=agency
            )
            lead.save()
            msg.lead = lead
            msg.is_lead_source = True
            msg.save()
            lead_created = True
        except Exception as e:
            logger.error('Message id: {0} qualified as a lead but could not be saved, Error: {1}'.format(msg.id, repr(e)))
            return '', False

    ### If we have a property and is not in the related list we add it ######
    if property:
        # check if there is already that property attached to the lead for the same dates, otherwise we add one
        lp, lp_created = LeadProperty.objects.get_or_create(
            lead=lead,
            property=property,
            agency=source.agency,
            available_from= msg_arrival or lead.arrival,
            available_to=msg_departure or lead.departure,
            defaults={'status': LeadProperty.REQUESTED}
        )
        if lp_created:  # Property not already on the list New offer must be sent
            lead.first_response = False

    ################ Notify if we created this lead, otherwise is a response ####################
    if lead_created:
        content = 'New lead from {0}'.format(lead.customer)
        notify(msg, content)
    else:
        msg.lead = lead
        msg.save()
        lead.modified = timezone.now()
        lead.save()
        logger.debug('Message id:{0} is a double post or a generic message from customer'.format(msg.id))
        content = 'New lead from {0}'.format(lead.customer)
        notify(msg, content)
    return lead, lead_created

def is_a_lead(sources, msg):
    """
    First we want to know if a message is a lead, for now we check if the subject qualifies and
    there is a 'signature' of the source somewhere in the message

    Keyword arguments:
    :param sources  list        list of active sources of an agency
    :param msg      object      a django mailbox Message object

    :return is_lead boolean     True if there is a match
    :return source
    """
    source_name = ''
    for source in sources:
        for rule in get_rules(source, target_field=SOURCE):  # We can have more rules to match to identify a source
            source_name = match_rule(msg, rule)
        for rule in get_rules(source, target_field=SUBJECT):  # And also there could be more subject rules
            subject = match_rule(msg, rule)
            if subject and source_name:
                return True, source
            elif not source_name and subject:
                logger.warning('Subject in message id: {0} matched but the source name did not'
                             ' match! Regex: '.format(msg.id, rule.regex))
            elif source_name and not subject:
                logger.warning('Source found in message id: {0} matched but the subject name did not'
                             ' match! Regex: '.format(msg.id, rule.regex))

    return False, ''  # Nothing matched,


def get_sources(msg, priority=0):
    """

    :param priority:
    :param msg:
    :return:
    """
    sources = []

    for agency in msg.mailbox.agency_set.all():
        for source in agency.sources.filter(active=True, priority=priority):
            sources.append(source)
    if not sources:
        logger.debug('No agency for this mailbox or no active rules, nothing to do for this message')
    return sources


def get_customer_id(email_address, source=None):
    """
    Returns, if matched the pk of a known customer.
    The tuples are cached, this will avoid hitting too much the database and increase performance.

    :param email_address:
    :return: Returns a customer id if matched, otherwise will be False
    """
    from leads.models import Customer
    # email_address = email_address.lower()
    # if CACHING_ENABLED:
    #     key = 'customers_emails'
    #     customers_emails = cache.get(key)
    #     if not customers_emails:
    #         customers_emails = Customer.objects.all().values_list('id', 'email')
    #         cache.set(key, customers_emails, CACHE_TIMEOUT)
    # else:
    #     customers_emails = Customer.objects.all().values_list('id', 'email')

    try:
        if source:
            customer = Customer.objects.filter(email__iexact=email_address, agency=source.agency)[0]
        else:
            customer = Customer.objects.filter(email__iexact=email_address)[0]
    except IndexError:
        return
    except Exception as e:
        logger.debug('Exception while getting customer'.format(repr(e)))
    else:
        return customer.pk


def update_customers_cache():
    """
    Here we clean the emails cache, typically when a new

    :return:
    """
    from leads.models import Customer
    if CACHING_ENABLED:
        key = 'customers_emails'
        customers_emails = Customer.objects.all().values_list('id', 'email')
        cache.set(key, customers_emails, CACHE_TIMEOUT)


def manage_generic_customer_message(msg, customer_id):
    """

    :param msg:
    :param customer_id:
    :return:
    """
    from leads.models import Lead, Customer
    leads = Lead.objects.filter(customer_id=customer_id).order_by('-modified')
    if leads.exists():
        lead = leads[0]
        msg.lead = lead
        msg.save()
        lead.modified = timezone.now()
        content = 'Reply from {0}'.format(lead.customer)
        lead.hot = True
        lead.save()
        notify(msg, content, alert=True)
    else: # a message from a client but no leads, lets create one or update an old one
        customer = Customer.objects.get(pk=customer_id)
        create_lead(source=None, msg=msg, customer=customer)
    return


def has_related_lead(msg, sources):
    """
    Obtaining the standard python email object we can check if the message has an 'In-Reply-To' field or a
    'References' so can be related to a lead if exists. We can implement another strategy to identify responses
    like testing the sender address and other lead related indicators.
    :param msg: mailbox Message
    :param sources:
    :return: True or False
    """
    # Let's see if we find a related message, linked or with a matching 'In-Reply-To' or 'References' header
    ref_msg = None
    source = None
    if msg.in_reply_to:  # we test if there is already a related message
        ref_msg = msg.in_reply_to
    else:
        message_obj = msg.get_email_object()
        message_id = False

        if 'In-Reply-To' in message_obj:
            message_id = message_obj['In-Reply-To']
        elif 'References' in message_obj:
            message_id = message_obj['References']

        if message_id:
            try:
                from django_mailbox.models import Message
                ref_msg = Message.objects.get(message_id=message_id)
            except msg.DoesNotExist:
                logger.debug('Message with internal id {0} that refers to id:\n{1}\n'
                             'has no matching messages.'.format(msg.id, message_id))
        # We want to see if there is already a lead or we can create one
    if ref_msg and ref_msg.lead:
        msg.lead = ref_msg.lead
        msg.save()
        content = 'Reply from {0}'.format(msg.lead.customer)
        notify(msg, content, alert=True)
        l = ref_msg.lead
        l.hot = True
        l.save()
        return True
    if ref_msg:
        is_lead, source = is_a_lead(sources, ref_msg)
        if is_lead:  # We had a reply to a potential lead but for some reason that was not qualified
            lead, lead_created = create_lead(source, ref_msg) # Forcing to create a lead
            msg.lead = lead
            msg.save()
            content = 'Reply from {0}'.format(msg.lead.customer)
            notify(msg, content, alert=True)
            lead.hot = True
            lead.save()
            return

    # Here we try to relate emails incoming from known customers to the last active lead
    if isinstance(msg.from_address, list):
        from_email = get_valid_email(' '.join(msg.from_address))
    else:
        from_email = get_valid_email(msg.from_address)
    if from_email:
        customer_id = get_customer_id(from_email, source)
        if customer_id:
            manage_generic_customer_message(msg, customer_id)
            return True
    return False


def check_email_for_lead(sender=None, message=None, instance=None, **kwargs):
    """
    Function to receive leads, multiple arguments so to be compatible either for
    django signals so for mailbox signal. The mailbox signal seems not to work
    so the process_incoming_message method is overridden to call this function directly.
    We had anyway to override the _process_message method so please be

    :type sender: object
    :param instance: typy
    :param kwargs:
    :param message:
    :param sender:
    Keyword arguments:
    :param msg:     a django mailbox Message object

    :return: None  nothing to return
    """
    if message:
        msg = message
    elif instance:
        msg = instance
    else:
        logger.warning('Got a signal without the instance!')
        return
    if msg.lead: # It's a lead source
        logger.debug('Message id: {0} is already referenced to a lead.\nSubject: {1}'.format(msg.id, msg.subject))
        return
    sources = get_sources(msg)
    if not sources:
        return  # No agency for this mailbox or no active rules, nothing to do for this message!

    is_lead, source = is_a_lead(sources, msg)

    if is_lead:
        create_lead(source, msg)
        return

    if has_related_lead(msg, sources):
        return  # A related lead has been found , don't need to continue

    for i in range(1,11):
        other_sources = get_sources(msg, priority=i)
        if not other_sources:
            continue
        is_lead, source = is_a_lead(other_sources, msg)
        if is_lead:
            create_lead(source, msg)
            return

    logger.info('Message id: {0} not a lead nor a reply.\nFrom: {1}\nSubject: {2}'.format(msg.id,
                                                                                             msg.from_address,
                                                                                             msg.subject))



#from django.db.models.signals import post_save
#from fetchmyguest.utils.email import message_received
#message_received.connect(check_email_for_lead, sender=Message, dispatch_uid='check_email')
#post_save.connect(check_email_for_lead, sender=Message, dispatch_uid='check_email')