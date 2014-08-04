#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
import ujson as json
import copy
from os import path
from events_logger.models import LogEvents, log_to_object, timestamp_to_datetime, datetime_to_timestamp
import logging

from celery.task import task

logger = logging.getLogger('')


def set_metadata(email_message, out_message):
    """

    :param email_message:
    :param out_message:
    :return:
    """
    try:
        email_message.metadata = [LogEvents.object_to_instance_metadata(out_message),
                                  LogEvents.object_to_instance_metadata(out_message.lead)]
    except Exception as e:
        logger.error('Error: {0}'.format(repr(e)))
    return email_message

@task()
def log_to_file(data, type=''):
    """

    :param data:
    :param type:
    """
    if settings.DEBUG:
        try:
            filename = path.join(settings.PROJECT_DIR, 'mandrillout-{0}.log'.format(type))
            with open(filename, mode='a') as file:
                file.write(json.dumps(data) + '\n')
        except IOError:
            logger.debug('cannot open file for append!')

@task()
def mandrill_to_objs(data, event_type):
    """

    :param data:
    :param description:
    :param event_type:
    """
    from django_mailbox.models import Message
    from leads.models import Lead, Customer
    description = ''
    extra_payload=None
    if event_type == 'send' or event_type == 'spam' or event_type == 'reject':
        description = get_description(data, 'Is set as {0}'.format(data.get('state')))
    if event_type == 'bounce':
        description = get_description(data, 'Bounced with reason: {0}'.format(data.get('bounce_description')))
    if event_type == 'open':
        description = get_description(data, 'Has been opened {0} times'.format(len(data.get('opens', ['', ]))))
        extra_payload = data.get('opens')
    if event_type == 'click':
        description = get_description(data, 'Has been clicked {0} times'.format(len(data.get('clicks', ['', ]))))
        extra_payload = data.get('clicks')

    objs = []

    for instance_metadata in data.get('metadata', []):
        try:
            obj = LogEvents.get_object(instance_metadata)
            objs.append(obj)
        except Exception as e:
            logger.error('Error in getting the event related obj: {0}'.format(repr(e)))

    if not objs:
        logger.info('No related objects found, ')
        return
    customer = None
    agency = None
    objs_to_log = []

    for i, obj in enumerate(objs):
        if isinstance(obj, (Lead, Message)):
            rel_objs = copy.copy(objs)
            to_obj = rel_objs.pop(i)
            if not agency:
                if isinstance(to_obj, Lead):
                    agency = to_obj.agency
                else:
                    try:
                        agency = to_obj.mailbox.agency_set.all()[0]
                    except:
                        pass

            if not customer and data.get('email') and agency:
                try:
                    customer = Customer.objects.get(email=data.get('email'), agency=agency)
                except:
                    customer = None
            objs_to_log.append((to_obj, rel_objs))
    for obj, rel_objs in objs_to_log:
        log_to_object(obj=obj,
                      field='events',
                      source='mandrill',
                      description=description,
                      events_type=event_type,
                      date=timestamp_to_datetime(data.get('ts')),
                      rel_objects=rel_objs,
                      actor=customer,
                      extra_payload=extra_payload
                      )



def get_description(msg, action_prhase):
    """

    :param msg:
    :param action_prhase:
    :return:
    """
    description = \
"""
Email to: {0}
Subject: {1}
{2} on: {3}
"""\
            .format(msg.get('email'),
                    msg.get('subject'),
                    action_prhase,
                    str(timestamp_to_datetime(msg.get('ts')))
                    )
    return description
