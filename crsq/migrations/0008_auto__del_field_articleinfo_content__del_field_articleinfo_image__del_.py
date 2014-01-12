# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ArticleInfo.content'
        db.delete_column(u'crsq_articleinfo', 'content')

        # Deleting field 'ArticleInfo.image'
        db.delete_column(u'crsq_articleinfo', 'image')

        # Deleting field 'ArticleInfo.title'
        db.delete_column(u'crsq_articleinfo', 'title')

        # Adding field 'ArticleInfo.articletitle'
        db.add_column(u'crsq_articleinfo', 'articletitle',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100L),
                      keep_default=False)

        # Adding field 'ArticleInfo.articleimage'
        db.add_column(u'crsq_articleinfo', 'articleimage',
                      self.gf('django.db.models.fields.TextField')(default=None, max_length=100L),
                      keep_default=False)

        # Adding field 'ArticleInfo.articlecontent'
        db.add_column(u'crsq_articleinfo', 'articlecontent',
                      self.gf('django.db.models.fields.TextField')(default=None),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ArticleInfo.content'
        raise RuntimeError("Cannot reverse this migration. 'ArticleInfo.content' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleInfo.content'
        db.add_column(u'crsq_articleinfo', 'content',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ArticleInfo.image'
        raise RuntimeError("Cannot reverse this migration. 'ArticleInfo.image' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleInfo.image'
        db.add_column(u'crsq_articleinfo', 'image',
                      self.gf('django.db.models.fields.TextField')(max_length=100L),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ArticleInfo.title'
        raise RuntimeError("Cannot reverse this migration. 'ArticleInfo.title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleInfo.title'
        db.add_column(u'crsq_articleinfo', 'title',
                      self.gf('django.db.models.fields.CharField')(max_length=100L),
                      keep_default=False)

        # Deleting field 'ArticleInfo.articletitle'
        db.delete_column(u'crsq_articleinfo', 'articletitle')

        # Deleting field 'ArticleInfo.articleimage'
        db.delete_column(u'crsq_articleinfo', 'articleimage')

        # Deleting field 'ArticleInfo.articlecontent'
        db.delete_column(u'crsq_articleinfo', 'articlecontent')


    models = {
        u'crsq.amazonprod': {
            'Meta': {'unique_together': "(('text', 'index'),)", 'object_name': 'AmazonProd'},
            'amazonlink': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_index': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'crsq.articleinfo': {
            'Meta': {'object_name': 'ArticleInfo'},
            'articlecontent': ('django.db.models.fields.TextField', [], {}),
            'articleimage': ('django.db.models.fields.TextField', [], {'max_length': '100L'}),
            'articletitle': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'fbpower': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'twitterpower': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100L', 'db_index': 'True'})
        },
        u'crsq.contentaffiliate': {
            'Meta': {'object_name': 'ContentAffiliate'},
            'affiliate': ('django.db.models.fields.TextField', [], {}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'null': 'True'}),
            'contenthash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100L', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'crsq.twitterlinks': {
            'Meta': {'object_name': 'TwitterLinks'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tweetid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'twitterlist': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'twitteruser': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_index': 'True'})
        }
    }

    complete_apps = ['crsq']