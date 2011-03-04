# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Category.keywords'
        db.alter_column('categories_category', 'keywords', self.gf('django.db.models.fields.TextField')(max_length=500))

        # Changing field 'Category.name'
        db.alter_column('categories_category', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))


    def backwards(self, orm):
        
        # Changing field 'Category.keywords'
        db.alter_column('categories_category', 'keywords', self.gf('django.db.models.fields.TextField')(max_length=300))

        # Changing field 'Category.name'
        db.alter_column('categories_category', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))


    models = {
        'categories.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['categories']
