# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Category.keywords'
        db.add_column('categories_category', 'keywords', self.gf('django.db.models.fields.TextField')(default='', max_length=300, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Category.keywords'
        db.delete_column('categories_category', 'keywords')


    models = {
        'categories.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['categories']
