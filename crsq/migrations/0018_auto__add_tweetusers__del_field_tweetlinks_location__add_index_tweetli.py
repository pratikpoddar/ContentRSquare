# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'TwitterListLinks', fields ['sector', 'twitteruser', 'twitterlist', 'tweetid']
        db.delete_unique(u'crsq_twitterlistlinks', ['sector', 'twitteruser', 'twitterlist', 'tweetid'])

        # Adding model 'TweetUsers'
        db.create_table(u'crsq_tweetusers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sector', self.gf('django.db.models.fields.CharField')(max_length=100L, db_index=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100L, db_index=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100L, db_index=True)),
        ))
        db.send_create_signal(u'crsq', ['TweetUsers'])

        # Deleting field 'TweetLinks.location'
        db.delete_column(u'crsq_tweetlinks', 'location')

        # Adding index on 'TweetLinks', fields ['author']
        db.create_index(u'crsq_tweetlinks', ['author'])

        # Deleting field 'TwitterListLinks.sector'
        db.delete_column(u'crsq_twitterlistlinks', 'sector')

        # Adding unique constraint on 'TwitterListLinks', fields ['twitteruser', 'twitterlist', 'tweetid']
        db.create_unique(u'crsq_twitterlistlinks', ['twitteruser', 'twitterlist', 'tweetid'])


    def backwards(self, orm):
        # Removing unique constraint on 'TwitterListLinks', fields ['twitteruser', 'twitterlist', 'tweetid']
        db.delete_unique(u'crsq_twitterlistlinks', ['twitteruser', 'twitterlist', 'tweetid'])

        # Removing index on 'TweetLinks', fields ['author']
        db.delete_index(u'crsq_tweetlinks', ['author'])

        # Deleting model 'TweetUsers'
        db.delete_table(u'crsq_tweetusers')

        # Adding field 'TweetLinks.location'
        db.add_column(u'crsq_tweetlinks', 'location',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=500L, null=True),
                      keep_default=False)

        # Adding field 'TwitterListLinks.sector'
        db.add_column(u'crsq_twitterlistlinks', 'sector',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100L),
                      keep_default=False)

        # Adding unique constraint on 'TwitterListLinks', fields ['sector', 'twitteruser', 'twitterlist', 'tweetid']
        db.create_unique(u'crsq_twitterlistlinks', ['sector', 'twitteruser', 'twitterlist', 'tweetid'])


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
            'articledate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'articlehtml': ('django.db.models.fields.TextField', [], {}),
            'articleimage': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1000L', 'null': 'True'}),
            'articletitle': ('django.db.models.fields.CharField', [], {'max_length': '1000L'}),
            'fbpower': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300L', 'null': 'True', 'blank': 'True'}),
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
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_index': 'True'})
        },
        u'crsq.contentaffiliate': {
            'Meta': {'object_name': 'ContentAffiliate'},
            'affiliate': ('django.db.models.fields.TextField', [], {}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'null': 'True'}),
            'contenthash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100L', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'crsq.importanttags': {
            'Meta': {'object_name': 'ImportantTags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255L'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255L'}),
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
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweetid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_index': 'True'})
        },
        u'crsq.tweetusers': {
            'Meta': {'object_name': 'TweetUsers'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_index': 'True'}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_index': 'True'})
        },
        u'crsq.twitterkeywordlinks': {
            'Meta': {'unique_together': "(('keyword', 'tweetid'),)", 'object_name': 'TwitterKeywordLinks'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tweetid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        },
        u'crsq.twitterlistlinks': {
            'Meta': {'unique_together': "(('twitteruser', 'twitterlist', 'tweetid'),)", 'object_name': 'TwitterListLinks'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tweetid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'twitterlist': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            'twitteruser': ('django.db.models.fields.CharField', [], {'max_length': '100L'})
        }
    }

    complete_apps = ['crsq']