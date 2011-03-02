# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Category.slug'
        db.delete_column('categories_category', 'slug')


    def backwards(self, orm):
        
        # Adding field 'Category.slug'
        db.add_column('categories_category', 'slug', self.gf('django.db.models.fields.SlugField')(default='slug000', max_length=50, db_index=True), keep_default=False)


    models = {
        'categories.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['categories']
