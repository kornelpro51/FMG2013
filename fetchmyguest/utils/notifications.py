from __future__ import unicode_literals
from __future__ import absolute_import
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from agencies.models import Notification
from fetchmyguest.utils.redis_utils import get_redis_connection

import logging

from leads.sockets import get_room_chan_name

logger = logging.getLogger('')


def notify(obj, content, alert=False):
    """
    Positional Arguments

    :param alert: whether or not must pop an alert
    :param obj      object      Whatever Django Model Object
    :param content  textfield      A string to be notified
    """
    from leads.serializers import NotificationSerializer
    from django_mailbox.models import Message
    from leads.models import Lead
    from django.db import transaction

    # We don't notify an old lead
    #try:
    #    if obj.lead.arrival < timezone.now().date():
    #        return
    #except Exception as e:
    #    pass

    notification = Notification(
        content_object=obj,
        content=content,
        alert=alert
    )
    if notification.alert:
        with transaction.commit_manually():
            try:

                notification.save(force_insert=True)

            except Exception as e:
                transaction.rollback()
                logger.error('Could not save the notification\n'
                             'Error: {0}'.format(str(e)))
                return
            transaction.commit()
    try:
        if notification.content_type == ContentType.objects.get_for_model(Message):
            ser = NotificationSerializer(instance=notification)
            data = JSONRenderer().render(ser.data)
            r = get_redis_connection()
            room = 'agency{0}_room'.format(notification.agency_id)
            r.publish(room, data)
        if notification.content_type == ContentType.objects.get_for_model(Lead):
            ser = NotificationSerializer(instance=notification)
            data = JSONRenderer().render(ser.data)
            r = get_redis_connection()
            room = 'agency{0}_room'.format(notification.agency_id)
            r.publish(room, data)

        logger.debug(
            'Notification for object: {0}\n'
            'Comment: {1}'.format(obj, notification))
    except Exception as e:
        logger.error('Could not push the notification\n'
                     'Error: {0}'.format(str(e)))