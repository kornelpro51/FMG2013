#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import ujson as json
import logging
from datetime import datetime
from django.utils import timezone
import time
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger('')


class LogEvents(object):
    """
    This class allows to manage and store events associated to Django objects in JSON format

    :param events_type: A reference name for the type of stored events
    :param counter: The number of stored events
    :param events: a List of events
    """
    events_type = ''
    counter = 0
    events = []

    def __init__(self, events_type='', counter=0, events=None):
        self.events_type = events_type
        if not isinstance(events, list):
            events = []
        self.events = events
        self.counter = counter

    @staticmethod
    def get_object(instance_metadata):
        """
        Given a dictionary that is composed by the Django App label, model name, and object id returns the object.
        This form:
        {app_label:'app label' , model: 'model name', object_id: 'object id' }
        :param instance_metadata:
        :return: returns the actual Django object
        """
        if instance_metadata:
            try:
                app_label = instance_metadata.get('app_label')
                model = instance_metadata.get('model')
                object_id = int(instance_metadata.get('object_id'))
                return ContentType.objects.get(app_label=app_label, model=model).get_object_for_this_type(pk=object_id)
            except Exception as e:
                logger.debug('Error getting the object: {0}'.format(repr(e)))
                return None
        else:
            return None

    @staticmethod
    def _get_event(event):
        return dict(date=timestamp_to_datetime(event.get('ts')),
                    description=event.get('desc', ''),
                    actor=LogEvents.get_object(instance_metadata=event.get('actor', '')),
                    rel_objects=[LogEvents.get_object(instance_metadata=o) for o in event.get('rel_objects')],
                    extra_payload=event.get('extra_payload', ''),
                    )

    @staticmethod
    def object_to_instance_metadata(obj):
        """
        Given a Django Model Object returns a dictionary that resembles the object in this form:
        {app_label:'app label' , model: 'model name', object_id: 'object id' }
        :param obj: a Django Model Object
        :return: dictionary
        """
        try:
            ct = ContentType.objects.get_for_model(obj)
            return dict(
                app_label=ct.app_label,
                model=ct.model,
                object_id=obj.pk
            )
        except:
            return None

    @staticmethod
    def _event_to_dict_ts(event):
        rel_objects = []
        for rel_objs in event.get('rel_objects'), []:
            for rel_obj in rel_objs:
                rel_objects.append(LogEvents.object_to_instance_metadata(rel_obj))
        return dict(ts=datetime_to_timestamp(event.get('date')),
                    desc=event.get('description'),
                    actor=LogEvents.object_to_instance_metadata(event.get('actor')) or '',
                    rel_objects=rel_objects,
                    extra_payload=event.get('extra_payload', ''),
                    )

    @staticmethod
    def _event_to_dict_dt(event):
        rel_objects = []
        for rel_objs in event.get('rel_objects'), []:
            for rel_obj in rel_objs:
                rel_objects.append(LogEvents.object_to_instance_metadata(rel_obj))
        return dict(date=event.get('date'),
                    desc=event.get('description'),
                    actor=LogEvents.object_to_instance_metadata(event.get('actor')) or '',
                    rel_objects=rel_objects,
                    extra_payload=event.get('extra_payload', ''),
                    )

    @classmethod
    def from_json(cls, json_data):
        """
        This @classmethod is to quick generate a LogEvents object out of a JSON string
        :param json_data:
        :return: Returns a LogEvents object
        """
        try:
            data = json.loads(json_data)
        except:
            logger.debug('No valid JSON data.')
            return None
        try:
            events_type = data.get('events_type')
            counter = data.get('counter')
            events = [cls._get_event(event=e) for e in data.get('events', [])]
            obj = cls(events_type=events_type, counter=counter, events=events)
        except Exception as e:
            logger.debug('Not a valid LogEvents object: {0}'.format(repr(e)))
            obj = None
        return obj

    def to_dict(self):
        """
        Method to return a dict() of the logged events

        :return:
        """
        log_dict = dict(events_type=self.events_type,
                        counter=len(self.events),
                        events=[LogEvents._event_to_dict_dt(e) for e in self.events]
                        )
        return log_dict

    def to_json(self):
        """
        Method to return a JSON string of the logged events

        :return: Returns JSON
        """
        log_dict = dict(events_type=self.events_type,
                        counter=len(self.events),
                        events=[LogEvents._event_to_dict_ts(e) for e in self.events]
                        )
        return json.dumps(log_dict)

    def add_event(self, description='', actor='', rel_objects=None, date=None, ts=None,  extra_payload=None):
        """
        This method to append an event

        :param description: A string to describe the event
        :param actor: If existing a user that generated the event
        :param rel_objects: Objects impacted by the event
        :param date: A datetime of the event
        :param ts: A unix timestamp of the event, overrides the date param
        :param extra_payload: extra JSON data
        """

        if ts:
            date = timestamp_to_datetime(ts)

        if not date:
            date = timezone.now()

        if not isinstance(rel_objects, list):
            rel_objects = []

        self.events.append(
            dict(description=description,
                 actor=actor,
                 rel_objects=rel_objects,
                 date=date,
                 extra_payload=extra_payload
                 )
        )
        self.counter = len(self.events)


def log_to_object(obj, field, source, description, events_type, date, rel_objects=None, actor=None, extra_payload=None):
    """

    :param obj:
    :param field:
    :param source:
    :param description:
    :param events_type:
    :param date:
    :param rel_objects:
    :param actor:
    :param extra_payload:
    """
    item = '{0}_{1}'.format(source, events_type)
    json_data = getattr(obj, field).get(item)
    logs = None
    if not isinstance(rel_objects, list):
        rel_objects = []
    if json_data:
        try:
            json.dumps(json_data)
            try:
                logs = LogEvents.from_json(json_data)
            except:
                pass
        except:
            pass
    if not logs:
        logs = LogEvents(events_type=events_type)

    logs.add_event(
        description=description,
        actor=actor,
        rel_objects=rel_objects,
        date=date,
        extra_payload=extra_payload
    )
    getattr(obj, field)[item] = logs.to_json()
    obj.save()


def timestamp_to_datetime(ts):
    """

    :param ts: unix timestamp
    :return: datetime.datetime
    """
    try:
        return datetime.fromtimestamp(int(ts))
    except:
        return timezone.now()


def datetime_to_timestamp(dt):
    """

    :param dt: datetime.datetime
    :return: unix timestamp
    """
    try:
        return int(time.mktime(dt.timetuple()))
    except:
        dt = timezone.now()
        return int(time.mktime(dt.timetuple()))