#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase
from django.test.utils import override_settings

import factory
from factory.django import DjangoModelFactory

from django.utils import crypto
from django.conf import settings
from leads.models import Lead, Customer, Property, LeadProperty, Note

class CustomerFactory(DjangoModelFactory):
    FACTORY_FOR = Customer



class LeadFactory(DjangoModelFactory):
    FACTORY_FOR = Lead
    FACTORY_DJANGO_GET_OR_CREATE = ('customer', 'source','organization')

class LeadFactory(DjangoModelFactory):
    FACTORY_FOR = Lead



class PeopleFactory(DjangoModelFactory):
    FACTORY_FOR = People
    FACTORY_DJANGO_GET_OR_CREATE = ('state_id', 'sis_id','organization')
    sis_id = factory.Sequence(lambda n: 'sis_id{0}'.format(str(n)))
    state_id = factory.Sequence(lambda n: 'state_id{0}'.format(str(n)))
    first_name = factory.Sequence(lambda n: 'first_name{0}'.format(str(n)))
    last_name = factory.Sequence(lambda n: 'last_name{0}'.format(str(n)))
    organization = factory.Sequence(lambda n: '{0}'.format(str(n)))
    role = 'student'
    password = rnd_psw()


#@override_settings(BASE_INUM=settings.TEST_BASE_INUM)
class PeopleTest(TestCase):
    @classmethod
    def setUpClass(cls):
        for p in People.objects.all():
            p.delete()
        db_ops(cls)
        ldap_ops(cls)
        cls.p1 = PeopleFactory(sis_id='aaa1', school='school1_district1', organization='district1', first_name='First', last_name='Last')
        cls.p2 = PeopleFactory(sis_id='aaa2', state_id='aaa2', organization='district1', school='school1_district1')

    def setUp(self):
        db_ops(self)

    def test_get_username(self):
        self.assertEqual(People.objects.get(username='district1_d_admin'), People.objects.get(sis_id='district1_d_admin'))

    def test_common_name(self):
        self.assertEqual(self.p1.common_name, 'First Last')

    def test_inum(self):
        self.assertTrue(settings.BASE_INUM in self.p1.inum)
        self.assertTrue(settings.BASE_INUM in self.p2.inum)
        self.assertFalse(self.p1.inum == self.p2.inum)

    # def test_delete(self):
    #     PeopleFactory.create(sis_id='aaa3')
    #     p = People.objects.get(sis_id='aaa3')
    #     p.delete()
    #     self.assertRaises(ObjectDoesNotExist, lambda: People.objects.get(sis_id='aaa3'))

    def test_unique_fields(self):
        p = People(sis_id='aaa2', state_id='aaa5', organization='district1', school='school1_district1', first_name='First', last_name='Last')
        self.assertRaises(IntegrityError, lambda: p.save())
        p = People(sis_id='aaa5', state_id='aaa2', organization='district1', school='school1_district1', first_name='First', last_name='Last')
        self.assertRaises(IntegrityError, lambda: p.save())

    @classmethod
    def tearDownClass(cls):
        for p in People.objects.all():
            p.delete()