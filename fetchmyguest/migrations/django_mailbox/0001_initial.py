# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mailbox'
        db.create_table(u'django_mailbox_mailbox', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uri', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('from_email', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'django_mailbox', ['Mailbox'])

        # Adding model 'Message'
        db.create_table(u'django_mailbox_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mailbox', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages', to=orm['django_mailbox.Mailbox'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('message_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('in_reply_to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='replies', null=True, to=orm['django_mailbox.Message'])),
            ('from_header', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('to_header', self.gf('django.db.models.fields.TextField')()),
            ('outgoing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('processed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('read', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('lead', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages', null=True, to=orm['leads.Lead'])),
            ('is_lead_source', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'django_mailbox', ['Message'])

        # Adding model 'MessageAttachment'
        db.create_table(u'django_mailbox_messageattachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='attachments', null=True, to=orm['django_mailbox.Message'])),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'django_mailbox', ['MessageAttachment'])


    def backwards(self, orm):
        # Deleting model 'Mailbox'
        db.delete_table(u'django_mailbox_mailbox')

        # Deleting model 'Message'
        db.delete_table(u'django_mailbox_message')

        # Deleting model 'MessageAttachment'
        db.delete_table(u'django_mailbox_messageattachment')


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
        u'django_mailbox.mailbox': {
            'Meta': {'object_name': 'Mailbox'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uri': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'django_mailbox.message': {
            'Meta': {'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'from_header': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'to': u"orm['django_mailbox.Message']"}),
            'is_lead_source': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'null': 'True', 'to': u"orm['leads.Lead']"}),
            'mailbox': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': u"orm['django_mailbox.Mailbox']"}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'outgoing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'processed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'read': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'to_header': ('django.db.models.fields.TextField', [], {})
        },
        u'django_mailbox.messageattachment': {
            'Meta': {'object_name': 'MessageAttachment'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'attachments'", 'null': 'True', 'to': u"orm['django_mailbox.Message']"})
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

    complete_apps = ['django_mailbox']