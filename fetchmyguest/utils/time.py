from __future__ import unicode_literals
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.utils import timezone


def whole_day(date_obj):
    """
    Returns a tuple of two datetime instances: the beginning of today, and the
    end of today.
    """
    local_timezone = timezone.get_current_timezone()
    start = datetime.min.replace(year=date_obj.year, month=date_obj.month, day=date_obj.day)
    end = (start + timedelta(days=1)) - timedelta.resolution

    return local_timezone.localize(start), local_timezone.localize(end)


def get_month_day_range(date):
    """
    For a date 'date' returns the start and end date for the month of 'date'.

    Month with 31 days:
    >>> date = datetime.date(2011, 7, 27)
    >>> get_month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))

    Month with 28 days:
    >>> date = datetime.date(2011, 2, 15)
    >>> get_month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
    """
    last_day = date + relativedelta(day=1, months=+1, days=-1)
    first_day = date + relativedelta(day=1)
    start_first_day, end_first_day = whole_day(first_day)
    start_last_day, end_last_day = whole_day(last_day)

    return start_first_day, end_last_day
