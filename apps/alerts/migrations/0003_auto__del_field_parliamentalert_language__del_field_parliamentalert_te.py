# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ParliamentAlert.language'
        db.delete_column('alerts_parliamentalert', 'language')

        # Deleting field 'ParliamentAlert.text'
        db.rename_column('alerts_parliamentalert', 'text', 'text_en')

        # Adding field 'ParliamentAlert.text_ka'
        db.add_column('alerts_parliamentalert', 'text_ka', self.gf('django.db.models.fields.TextField')(default='', max_length=140), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'ParliamentAlert.language'
        raise RuntimeError("Cannot reverse this migration. 'ParliamentAlert.language' and its values cannot be restored.")

        # Deleting field 'ParliamentAlert.text_en'
        db.rename_column('alerts_parliamentalert', 'text_en', 'text')

        # Deleting field 'ParliamentAlert.text_ka'
        db.delete_column('alerts_parliamentalert', 'text_ka')


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
            'text_en': ('django.db.models.fields.TextField', [], {'max_length': '140'}),
            'text_ka': ('django.db.models.fields.TextField', [], {'max_length': '140'})
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
            'only_important': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['alerts']
