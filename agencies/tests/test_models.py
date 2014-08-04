#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase
from django.test.utils import override_settings

import factory
from factory.django import DjangoModelFactory
from agencies.models import Agency
from custom_user.models import EmailUser


class AgencyFactory(DjangoModelFactory):
    FACTORY_FOR = Agency
    FACTORY_DJANGO_GET_OR_CREATE = ('name','email')
    name = factory.Sequence(lambda n: 'Agency_{0}'.format(str(n)))
    email = factory.Sequence(lambda n: 'info@agency_{0}.com'.format(str(n)))

class UserFactory(DjangoModelFactory):
    FACTORY_FOR = Agency
    FACTORY_DJANGO_GET_OR_CREATE = ('name','email')