from __future__ import unicode_literals

def int_or_0(value):
    """
    Transform a sting into an integer without getting errors for empty strings
    Key params
    :param value can be a string

    :return zero or an integer
    """
    try:
        return int(value)
    except:
        return 0