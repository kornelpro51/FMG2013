#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import re


def get_valid_email(string, many=False):
    regex = re.compile(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:"
                       r"[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")"
                       r"@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|"
                       r"\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?"
                       r"|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]"
                       r"|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
    email = None
    try:
        results = regex.findall(string)
        if results:
            email = results
        if not many:
            email = results[0]
    except IndexError:
        pass
    finally:
        return email