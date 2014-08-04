# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RegExRule'
        db.create_table(u'agencies_regexrule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('matching_group', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('regex', self.gf('django.db.models.fields.TextField')()),
            ('example_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'agencies', ['RegExRule'])

        # Adding model 'Agency'
        db.create_table(u'agencies_agency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'], null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Region'], null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django_localflavor_us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('mailbox', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_mailbox.Mailbox'])),
            ('smtp_host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('smtp_port', self.gf('django.db.models.fields.IntegerField')()),
            ('smtp_user', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('smtp_password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('smtp_use_tls', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'agencies', ['Agency'])

        # Adding M2M table for field source_id on 'Agency'
        m2m_table_name = db.shorten_name(u'agencies_agency_source_id')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('agency', models.ForeignKey(orm[u'agencies.agency'], null=False)),
            ('regexrule', models.ForeignKey(orm[u'agencies.regexrule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['agency_id', 'regexrule_id'])

        # Adding M2M table for field lead_subject on 'Agency'
        m2m_table_name = db.shorten_name(u'agencies_agency_lead_subject')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('agency', models.ForeignKey(orm[u'agencies.agency'], null=False)),
            ('regexrule', models.ForeignKey(orm[u'agencies.regexrule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['agency_id', 'regexrule_id'])

        # Adding M2M table for field property_id on 'Agency'
        m2m_table_name = db.shorten_name(u'agencies_agency_property_id')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('agency', models.ForeignKey(orm[u'agencies.agency'], null=False)),
            ('regexrule', models.ForeignKey(orm[u'agencies.regexrule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['agency_id', 'regexrule_id'])

        # Adding M2M table for field arrival on 'Agency'
        m2m_table_name = db.shorten_name(u'agencies_agency_arrival')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('agency', models.ForeignKey(orm[u'agencies.agency'], null=False)),
            ('regexrule', models.ForeignKey(orm[u'agencies.regexrule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['agency_id', 'regexrule_id'])

        # Adding M2M table for field departure on 'Agency'
        m2m_table_name = db.shorten_name(u'agencies_agency_departure')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('agency', models.ForeignKey(orm[u'agencies.agency'], null=False)),
            ('regexrule', models.ForeignKey(orm[u'agencies.regexrule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['agency_id', 'regexrule_id'])

        # Adding M2M table for field customer_name on 'Agency'
        m2m_table_name = db.shorten_name(u'agencies_agency_customer_name')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('agency', models.ForeignKey(orm[u'agencies.agency'], null=False)),
            ('regexrule', models.ForeignKey(orm[u'agencies.regexrule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['agency_id', 'regexrule_id'])

        # Adding M2M table for field customer_email on 'Agency'
        m2m_table_name = db.shorten_name(u'agencies_agency_customer_email')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('agency', models.ForeignKey(orm[u'agencies.agency'], null=False)),
            ('regexrule', models.ForeignKey(orm[u'agencies.regexrule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['agency_id', 'regexrule_id'])

        # Adding model 'Agent'
        db.create_table(u'agencies_agent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mugshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('privacy', self.gf('django.db.models.fields.CharField')(default='registered', max_length=15)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['agencies.Agency'], null=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='agent_profile', unique=True, to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'], null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Region'], null=True, blank=True)),
            ('phone', self.gf('django_localflavor_us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('email_signature', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'agencies', ['Agent'])

        # Adding model 'EmailTemplate'
        db.create_table(u'agencies_emailtemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['agencies.Agency'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('html_template', self.gf('django.db.models.fields.TextField')()),
            ('text_template', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'agencies', ['EmailTemplate'])


    def backwards(self, orm):
        # Deleting model 'RegExRule'
        db.delete_table(u'agencies_regexrule')

        # Deleting model 'Agency'
        db.delete_table(u'agencies_agency')

        # Removing M2M table for field source_id on 'Agency'
        db.delete_table(db.shorten_name(u'agencies_agency_source_id'))

        # Removing M2M table for field lead_subject on 'Agency'
        db.delete_table(db.shorten_name(u'agencies_agency_lead_subject'))

        # Removing M2M table for field property_id on 'Agency'
        db.delete_table(db.shorten_name(u'agencies_agency_property_id'))

        # Removing M2M table for field arrival on 'Agency'
        db.delete_table(db.shorten_name(u'agencies_agency_arrival'))

        # Removing M2M table for field departure on 'Agency'
        db.delete_table(db.shorten_name(u'agencies_agency_departure'))

        # Removing M2M table for field customer_name on 'Agency'
        db.delete_table(db.shorten_name(u'agencies_agency_customer_name'))

        # Removing M2M table for field customer_email on 'Agency'
        db.delete_table(db.shorten_name(u'agencies_agency_customer_email'))

        # Deleting model 'Agent'
        db.delete_table(u'agencies_agent')

        # Deleting model 'EmailTemplate'
        db.delete_table(u'agencies_emailtemplate')


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
        u'agencies.agency': {
            'Meta': {'object_name': 'Agency'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'arrival': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'leads_arrivals'", 'null': 'True', 'to': u"orm['agencies.RegExRule']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']", 'null': 'True', 'blank': 'True'}),
            'customer_email': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'leads_customer_emails'", 'null': 'True', 'to': u"orm['agencies.RegExRule']"}),
            'customer_name': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'leads_customer_names'", 'null': 'True', 'to': u"orm['agencies.RegExRule']"}),
            'departure': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'leads_departures'", 'null': 'True', 'to': u"orm['agencies.RegExRule']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead_subject': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'leads_subjects'", 'symmetrical': 'False', 'to': u"orm['agencies.RegExRule']"}),
            'mailbox': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_mailbox.Mailbox']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django_localflavor_us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'property_id': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'leads_property_ids'", 'null': 'True', 'to': u"orm['agencies.RegExRule']"}),
            'smtp_host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'smtp_password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'smtp_port': ('django.db.models.fields.IntegerField', [], {}),
            'smtp_use_tls': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'smtp_user': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source_id': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'leads_agency_ids'", 'symmetrical': 'False', 'to': u"orm['agencies.RegExRule']"}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Region']", 'null': 'True', 'blank': 'True'})
        },
        u'agencies.agent': {
            'Meta': {'object_name': 'Agent'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['agencies.Agency']", 'null': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']", 'null': 'True', 'blank': 'True'}),
            'email_signature': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'phone': ('django_localflavor_us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Region']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'agent_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'agencies.emailtemplate': {
            'Meta': {'object_name': 'EmailTemplate'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['agencies.Agency']"}),
            'html_template': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'text_template': ('django.db.models.fields.TextField', [], {})
        },
        u'agencies.regexrule': {
            'Meta': {'object_name': 'RegExRule'},
            'example_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matching_group': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'regex': ('django.db.models.fields.TextField', [], {})
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
        u'django_mailbox.mailbox': {
            'Meta': {'object_name': 'Mailbox'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uri': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['agencies']