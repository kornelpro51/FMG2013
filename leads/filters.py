from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import timedelta
import django_filters
from agencies.models import Notification
from django_mailbox.models import Message
from leads.models import Lead, Note
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

_truncate = lambda dt: dt.replace(hour=0, minute=0, second=0)


class CustomDateRangeFilter(django_filters.DateRangeFilter):
    options = {
        '': (_('Default (Past 30 days)'), lambda qs, name: qs.filter(**{
            '%s__gte' % name: _truncate(now() - timedelta(days=30)),
            '%s__lt' % name: _truncate(now() + timedelta(days=1)),
        })),
        1: (_('Today'), lambda qs, name: qs.filter(
            **{
            '%s__year' % name: now().year,
            '%s__month' % name: now().month,
            '%s__day' % name: now().day
            })),
        2: (_('Past 7 days'), lambda qs, name: qs.filter(**{
            '%s__gte' % name: _truncate(now() - timedelta(days=7)),
            '%s__lt' % name: _truncate(now() + timedelta(days=1)),
        })),
        3: (_('Past 30 days'), lambda qs, name: qs.filter(**{
            '%s__gte' % name: _truncate(now() - timedelta(days=30)),
            '%s__lt' % name: _truncate(now() + timedelta(days=1)),
        })),
        4: (_('This month'), lambda qs, name: qs.filter(**{
            '%s__year' % name: now().year,
            '%s__month' % name: now().month
        })),
        5: (_('This year'), lambda qs, name: qs.filter(**{
            '%s__year' % name: now().year,
        })),
        6: (_('Any date'), lambda qs, name: qs.all()),
    }


class LeadFilterSet(django_filters.FilterSet):
    modified = CustomDateRangeFilter()

    class Meta:
        model = Lead
        fields = ['modified']

class MessageFilterSet(django_filters.FilterSet):
    lead_id = django_filters.NumberFilter()
    class Meta:
        model = Message
        fields = ['lead_id']

class NoteFilterSet(django_filters.FilterSet):
    lead_id = django_filters.NumberFilter()
    class Meta:
        model = Note
        fields = ['lead_id']

class NotificationFilterSet(django_filters.FilterSet):
    content_type = django_filters.NumberFilter()
    class Meta:
        model = Notification
        fields = ['content_type']