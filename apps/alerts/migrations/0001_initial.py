# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ParliamentAlert'
        db.create_table('alerts_parliamentalert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=140)),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('is_important', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent_date', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('alerts', ['ParliamentAlert'])

        # Adding M2M table for field categories on 'ParliamentAlert'
        db.create_table('alerts_parliamentalert_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parliamentalert', models.ForeignKey(orm['alerts.parliamentalert'], null=False)),
            ('category', models.ForeignKey(orm['categories.category'], null=False))
        ))
        db.create_unique('alerts_parliamentalert_categories', ['parliamentalert_id', 'category_id'])


    def backwards(self, orm):
        
        # Deleting model 'ParliamentAlert'
        db.delete_table('alerts_parliamentalert')

        # Removing M2M table for field categories on 'ParliamentAlert'
        db.delete_table('alerts_parliamentalert_categories')


    models = {
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['alerts']
