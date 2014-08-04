#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from dateutil.relativedelta import relativedelta
from agencies.models import Notification
from leads.models import Lead
from django.db.models import Q
from celery.task import task
from django.utils import timezone
from django_mailbox.models import Mailbox, Message
from django import db
from django.db import transaction

logger = logging.getLogger('')



@task(name='check_active_mailboxes', ignore_result=True)
def check_email():
    try:
        for m in Mailbox.objects.filter(active=True):
            m.get_new_mail()

            logger.debug('Checking {0} mailbox, email: {1}'.format(m, m.from_email))
    except Exception, e:
        logger.error('Got an error: {0}'.format(str(e)))
    return

@task(name='clean_old_messages', ignore_result=True)
def clean_email():
    r_date = timezone.now().date() + relativedelta(days=-30)
    try:
        Message.objects.filter(processed__lt=r_date).filter(lead__isnull=True).delete()
    except Exception, e:
        logger.error('Got an error: {0}'.format(str(e)))

    return

@task(name='clean_old_not_booked_leads', ignore_result=True)
def clean_old_leads():
    Lead.objects.filter(arrival__lt=timezone.now().date() + relativedelta(days=-30)).exclude(booked=True).delete()


@task(name='clean_old_notifications', ignore_result=True)
def clean_notifications():
    WHEN = timezone.now() + relativedelta(hours=-72)
    Notification.objects.filter(created__lt=WHEN).delete()

@task(name='switch_off_hot_leads', ignore_result=True)
def switch_off_hot_leads():
    WHEN = timezone.now() + relativedelta(days=-30)
    Lead.objects.filter((Q(modified__lt=WHEN)| Q(booked=True)) & Q(hot=True)).update(hot=False)
