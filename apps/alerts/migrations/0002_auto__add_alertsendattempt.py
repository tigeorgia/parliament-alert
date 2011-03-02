# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AlertSendAttempt'
        db.create_table('alerts_alertsendattempt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms.Contact'])),
            ('alert', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alerts.ParliamentAlert'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('alerts', ['AlertSendAttempt'])


    def backwards(self, orm):
        
        # Deleting model 'AlertSendAttempt'
        db.delete_table('alerts_alertsendattempt')


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
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['categories.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_important': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '140'})
        },
        'categories.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['categories.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'only_important': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['alerts']
