# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArticleTags'
        db.create_table(u'crsq_articletags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255L, db_index=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=255L, db_index=True)),
        ))
        db.send_create_signal(u'crsq', ['ArticleTags'])

        # Adding unique constraint on 'ArticleTags', fields ['url', 'tag']
        db.create_unique(u'crsq_articletags', ['url', 'tag'])

        # Deleting field 'ArticleSemantics.tags'
        db.delete_column(u'crsq_articlesemantics', 'tags')


    def backwards(self, orm):
        # Removing unique constraint on 'ArticleTags', fields ['url', 'tag']
        db.delete_unique(u'crsq_articletags', ['url', 'tag'])

        # Deleting model 'ArticleTags'
        db.delete_table(u'crsq_articletags')

        # Adding field 'ArticleSemantics.tags'
        db.add_column(u'crsq_articlesemantics', 'tags',
                      self.gf('django.db.models.fields.TextField')(default=None),
                      keep_default=False)


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
            'articledate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'articleimage': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1000L', 'null': 'True'}),
            'articletitle': ('django.db.models.fields.CharField', [], {'max_length': '1000L'}),
            'fbpower': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'twitterpower': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_index': 'True'})
        },
        u'crsq.articlesemantics': {
            'Meta': {'object_name': 'ArticleSemantics'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000L', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_index': 'True'})
        },
        u'crsq.articletags': {
            'Meta': {'unique_together': "(('url', 'tag'),)", 'object_name': 'ArticleTags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_index': 'True'})
        },
        u'crsq.contentaffiliate': {
            'Meta': {'object_name': 'ContentAffiliate'},
            'affiliate': ('django.db.models.fields.TextField', [], {}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'null': 'True'}),
            'contenthash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100L', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'crsq.penpatronuser': {
            'Meta': {'object_name': 'PenPatronUser'},
            'blog': ('django.db.models.fields.CharField', [], {'max_length': '1000L'}),
            'college': ('django.db.models.fields.CharField', [], {'max_length': '1000L'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255L'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1000L'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255L'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255L'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'crsq.tweetlinks': {
            'Meta': {'unique_together': "(('tweetid', 'url'),)", 'object_name': 'TweetLinks'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '500L', 'null': 'True'}),
            'tweetid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_index': 'True'})
        },
        u'crsq.twitterkeywordlinks': {
            'Meta': {'unique_together': "(('keyword', 'tweetid'),)", 'object_name': 'TwitterKeywordLinks'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tweetid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        },
        u'crsq.twitterlistlinks': {
            'Meta': {'unique_together': "(('sector', 'twitteruser', 'twitterlist', 'tweetid'),)", 'object_name': 'TwitterListLinks'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tweetid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'twitterlist': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'twitteruser': ('django.db.models.fields.CharField', [], {'max_length': '100L'})
        }
    }

    complete_apps = ['crsq']