# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContentAffiliate'
        db.create_table(u'crsq_contentaffiliate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contenthash', self.gf('django.db.models.fields.BigIntegerField')(unique=True, db_index=True)),
            ('affiliate', self.gf('picklefield.fields.PickledObjectField')()),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=100L, null=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'crsq', ['ContentAffiliate'])

        # Adding model 'AmazonProd'
        db.create_table(u'crsq_amazonprod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100L, db_index=True)),
            ('index', self.gf('django.db.models.fields.CharField')(max_length=100L)),
            ('amazonlink', self.gf('django.db.models.fields.CharField')(max_length=100L)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'crsq', ['AmazonProd'])

        # Adding unique constraint on 'AmazonProd', fields ['text', 'index']
        db.create_unique(u'crsq_amazonprod', ['text', 'index'])


    def backwards(self, orm):
        # Removing unique constraint on 'AmazonProd', fields ['text', 'index']
        db.delete_unique(u'crsq_amazonprod', ['text', 'index'])

        # Deleting model 'ContentAffiliate'
        db.delete_table(u'crsq_contentaffiliate')

        # Deleting model 'AmazonProd'
        db.delete_table(u'crsq_amazonprod')


    models = {
        u'crsq.amazonprod': {
            'Meta': {'unique_together': "(('text', 'index'),)", 'object_name': 'AmazonProd'},
            'amazonlink': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_index': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'crsq.contentaffiliate': {
            'Meta': {'object_name': 'ContentAffiliate'},
            'affiliate': ('picklefield.fields.PickledObjectField', [], {}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'null': 'True'}),
            'contenthash': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['crsq']