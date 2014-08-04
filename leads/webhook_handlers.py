#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from djrill.signals import webhook_event
from django.dispatch import receiver
from events_logger.mandrill_utils import log_to_file, mandrill_to_objs
import logging

logger = logging.getLogger('')

def handle_mandrill(sender, event_type, data, **kwargs):
    if event_type == 'hard_bounce' or event_type == 'soft_bounce':
        event_type = 'bounce'
    try:
        log_to_file(data, event_type)
        msg = data.get('msg', {})
        mandrill_to_objs.apply_async((msg, event_type))
    except Exception as e:
        logger.error('Error while logging Mandrll event:\n{0}'.format(repr(e)))
