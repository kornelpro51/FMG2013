# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'leads_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django_localflavor_us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'leads', ['Client'])

        # Adding model 'Property'
        db.create_table(u'leads_property', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'], null=True, blank=True)),
            ('property_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bathrooms', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bedrooms', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'leads', ['Property'])

        # Adding model 'Suggestion'
        db.create_table(u'leads_suggestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lead', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Lead'])),
            ('property_suggested', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Property'])),
            ('suggested_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('available_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('available_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'leads', ['Suggestion'])

        # Adding model 'Lead'
        db.create_table(u'leads_lead', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Client'])),
            ('asked_property', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leads', null=True, to=orm['leads.Property'])),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('arrival', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('departure', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('adults', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('children', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('phone_contact', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('first_response', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('second_response', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('offer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hot', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('booked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal(u'leads', ['Lead'])

        # Adding model 'Note'
        db.create_table(u'leads_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('lead', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Lead'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('read_on', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'leads', ['Note'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'leads_client')

        # Deleting model 'Property'
        db.delete_table(u'leads_property')

        # Deleting model 'Suggestion'
        db.delete_table(u'leads_suggestion')

        # Deleting model 'Lead'
        db.delete_table(u'leads_lead')

        # Deleting model 'Note'
        db.delete_table(u'leads_note')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cities_light.city': {
            'Meta': {'unique_together': "(('region', 'name'),)", 'object_name': 'City'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Region']", 'null': 'True', 'blank': 'True'}),
            'search_names': ('cities_light.models.ToSearchTextField', [], {'default': "''", 'max_length': '4000', 'db_index': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"})
        },
        u'cities_light.country': {
            'Meta': {'object_name': 'Country'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'code2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'code3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"}),
            'tld': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '5', 'blank': 'True'})
        },
        u'cities_light.region': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'Region'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'geoname_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'leads.client': {
            'Meta': {'object_name': 'Client'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('django_localflavor_us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'leads.lead': {
            'Meta': {'object_name': 'Lead'},
            'adults': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'arrival': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'asked_property': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leads'", 'null': 'True', 'to': u"orm['leads.Property']"}),
            'booked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'children': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Client']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'departure': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_response': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'hot': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'offer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_contact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'second_response': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'suggested_properties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'suggesting_leads'", 'null': 'True', 'through': u"orm['leads.Suggestion']", 'to': u"orm['leads.Property']"})
        },
        u'leads.note': {
            'Meta': {'object_name': 'Note'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Lead']"}),
            'read_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'leads.property': {
            'Meta': {'object_name': 'Property'},
            'bathrooms': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bedrooms': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'property_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'leads.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'available_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'available_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Lead']"}),
            'property_suggested': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Property']"}),
            'suggested_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['leads']