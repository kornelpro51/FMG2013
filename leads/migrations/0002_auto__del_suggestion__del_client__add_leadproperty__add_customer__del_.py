# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Suggestion'
        db.delete_table(u'leads_suggestion')

        # Deleting model 'Client'
        db.delete_table(u'leads_client')

        # Adding model 'LeadProperty'
        db.create_table(u'leads_leadproperty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lead', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Lead'])),
            ('property', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Property'])),
            ('available_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('available_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('suggested_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PR', max_length=2)),
        ))
        db.send_create_signal(u'leads', ['LeadProperty'])

        # Adding model 'Customer'
        db.create_table(u'leads_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('phone', self.gf('django_localflavor_us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'leads', ['Customer'])

        # Deleting field 'Property.capacity'
        db.delete_column(u'leads_property', 'capacity')

        # Deleting field 'Property.name'
        db.delete_column(u'leads_property', 'name')

        # Deleting field 'Property.source_id'
        db.delete_column(u'leads_property', 'source_id')

        # Adding field 'Property.title'
        db.add_column(u'leads_property', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Property.address'
        db.add_column(u'leads_property', 'address',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'Property.state'
        db.add_column(u'leads_property', 'state',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Region'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Property.sleeps'
        db.add_column(u'leads_property', 'sleeps',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Property.created'
        db.add_column(u'leads_property', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 6, 14, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Property.modified'
        db.add_column(u'leads_property', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 6, 14, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Note.read_on'
        db.delete_column(u'leads_note', 'read_on')

        # Deleting field 'Note.agent'
        db.delete_column(u'leads_note', 'agent_id')

        # Adding field 'Note.user'
        db.add_column(u'leads_note', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Note.modified'
        db.add_column(u'leads_note', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 6, 14, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Lead.asked_property'
        db.delete_column(u'leads_lead', 'asked_property_id')

        # Deleting field 'Lead.phone_contact'
        db.delete_column(u'leads_lead', 'phone_contact')

        # Deleting field 'Lead.client'
        db.delete_column(u'leads_lead', 'client_id')

        # Deleting field 'Lead.message'
        db.delete_column(u'leads_lead', 'message')

        # Deleting field 'Lead.from_email'
        db.delete_column(u'leads_lead', 'from_email')

        # Adding field 'Lead.customer'
        db.add_column(u'leads_lead', 'customer',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['leads.Customer']),
                      keep_default=False)


        # Changing field 'Lead.arrival'
        db.alter_column(u'leads_lead', 'arrival', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Lead.departure'
        db.alter_column(u'leads_lead', 'departure', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):
        # Adding model 'Suggestion'
        db.create_table(u'leads_suggestion', (
            ('suggested_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('property_suggested', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Property'])),
            ('available_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('lead', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Lead'])),
            ('available_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'leads', ['Suggestion'])

        # Adding model 'Client'
        db.create_table(u'leads_client', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django_localflavor_us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'leads', ['Client'])

        # Deleting model 'LeadProperty'
        db.delete_table(u'leads_leadproperty')

        # Deleting model 'Customer'
        db.delete_table(u'leads_customer')

        # Adding field 'Property.capacity'
        db.add_column(u'leads_property', 'capacity',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Property.name'
        db.add_column(u'leads_property', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Property.source_id'
        db.add_column(u'leads_property', 'source_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'Property.title'
        db.delete_column(u'leads_property', 'title')

        # Deleting field 'Property.address'
        db.delete_column(u'leads_property', 'address')

        # Deleting field 'Property.state'
        db.delete_column(u'leads_property', 'state_id')

        # Deleting field 'Property.sleeps'
        db.delete_column(u'leads_property', 'sleeps')

        # Deleting field 'Property.created'
        db.delete_column(u'leads_property', 'created')

        # Deleting field 'Property.modified'
        db.delete_column(u'leads_property', 'modified')

        # Adding field 'Note.read_on'
        db.add_column(u'leads_note', 'read_on',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Note.agent'
        db.add_column(u'leads_note', 'agent',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True),
                      keep_default=False)

        # Deleting field 'Note.user'
        db.delete_column(u'leads_note', 'user_id')

        # Deleting field 'Note.modified'
        db.delete_column(u'leads_note', 'modified')

        # Adding field 'Lead.asked_property'
        db.add_column(u'leads_lead', 'asked_property',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='leads', null=True, to=orm['leads.Property']),
                      keep_default=False)

        # Adding field 'Lead.phone_contact'
        db.add_column(u'leads_lead', 'phone_contact',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Lead.client'
        db.add_column(u'leads_lead', 'client',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['leads.Client']),
                      keep_default=False)

        # Adding field 'Lead.message'
        db.add_column(u'leads_lead', 'message',
                      self.gf('django.db.models.fields.TextField')(default=1),
                      keep_default=False)

        # Adding field 'Lead.from_email'
        db.add_column(u'leads_lead', 'from_email',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Lead.customer'
        db.delete_column(u'leads_lead', 'customer_id')


        # Changing field 'Lead.arrival'
        db.alter_column(u'leads_lead', 'arrival', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Lead.departure'
        db.alter_column(u'leads_lead', 'departure', self.gf('django.db.models.fields.DateTimeField')(null=True))

    models = {
        u'actstream.action': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Action'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_object'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'to': u"orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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
        u'leads.customer': {
            'Meta': {'object_name': 'Customer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('django_localflavor_us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'leads.lead': {
            'Meta': {'object_name': 'Lead'},
            'adults': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'arrival': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'booked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'children': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Customer']"}),
            'departure': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_response': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hot': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'offer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'properties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'proposing_leads'", 'null': 'True', 'through': u"orm['leads.LeadProperty']", 'to': u"orm['leads.Property']"}),
            'second_response': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'leads.leadproperty': {
            'Meta': {'object_name': 'LeadProperty'},
            'available_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'available_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Lead']"}),
            'property': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Property']"}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PR'", 'max_length': '2'}),
            'suggested_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'leads.note': {
            'Meta': {'object_name': 'Note'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Lead']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'leads.property': {
            'Meta': {'object_name': 'Property'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'bathrooms': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bedrooms': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'property_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'sleeps': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Region']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['leads']