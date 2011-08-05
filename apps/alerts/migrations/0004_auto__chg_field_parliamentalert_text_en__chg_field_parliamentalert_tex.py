# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ParliamentAlert.text_en'
        db.alter_column('alerts_parliamentalert', 'text_en', self.gf('django.db.models.fields.CharField')(max_length=150))

        # Changing field 'ParliamentAlert.text_ka'
        db.alter_column('alerts_parliamentalert', 'text_ka', self.gf('django.db.models.fields.CharField')(max_length=150))


    def backwards(self, orm):
        
        # Changing field 'ParliamentAlert.text_en'
        db.alter_column('alerts_parliamentalert', 'text_en', self.gf('django.db.models.fields.TextField')(max_length=140))

        # Changing field 'ParliamentAlert.text_ka'
        db.alter_column('alerts_parliamentalert', 'text_ka', self.gf('django.db.models.fields.TextField')(max_length=140))


    models = {
        'alerts.alertsendattempt': {
            'Meta': {'object_name': 'AlertSendAttempt'},
            'alert': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alerts.ParliamentAlert']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Contact']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'alerts.parliamentalert': {
            'Meta': {'object_name': 'ParliamentAlert'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['categories.Category']", 'symmetrical': 'False'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_important': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'text_en': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'text_ka': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'categories.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['categories.Category']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'only_important': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['alerts']
