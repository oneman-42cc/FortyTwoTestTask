# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models, connection


class Migration(SchemaMigration):

    def forwards(self, orm):

        if 'hello_profile' in connection.introspection.table_names():
            db.delete_table('hello_profile')

        # Adding model 'Profile'
        db.create_table(u'hello_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('jabber', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contacts_other', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('hello', ['Profile'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'hello_profile')


    models = {
        'hello.profile': {
            'Meta': {'object_name': 'Profile'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contacts_other': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        }
    }

    complete_apps = ['hello']