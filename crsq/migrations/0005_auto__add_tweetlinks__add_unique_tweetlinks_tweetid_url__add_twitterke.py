# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TweetLinks'
        db.create_table(u'crsq_tweetlinks', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweetid', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100L)),
            ('location', self.gf('django.db.models.fields.CharField')(default=None, max_length=100L, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100L, db_index=True)),
        ))
        db.send_create_signal(u'crsq', ['TweetLinks'])

        # Adding unique constraint on 'TweetLinks', fields ['tweetid', 'url']
        db.create_unique(u'crsq_tweetlinks', ['tweetid', 'url'])

        # Adding model 'TwitterKeywordLinks'
        db.create_table(u'crsq_twitterkeywordlinks', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=100L)),
            ('tweetid', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'crsq', ['TwitterKeywordLinks'])

        # Adding unique constraint on 'TwitterKeywordLinks', fields ['keyword', 'tweetid']
        db.create_unique(u'crsq_twitterkeywordlinks', ['keyword', 'tweetid'])

        # Adding model 'TwitterListLinks'
        db.create_table(u'crsq_twitterlistlinks', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sector', self.gf('django.db.models.fields.CharField')(max_length=100L)),
            ('twitteruser', self.gf('django.db.models.fields.CharField')(max_length=100L)),
            ('twitterlist', self.gf('django.db.models.fields.CharField')(max_length=100L)),
            ('tweetid', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'crsq', ['TwitterListLinks'])

        # Adding unique constraint on 'TwitterListLinks', fields ['sector', 'twitteruser', 'twitterlist', 'tweetid']
        db.create_unique(u'crsq_twitterlistlinks', ['sector', 'twitteruser', 'twitterlist', 'tweetid'])

        # Adding model 'ArticleInfo'
        db.create_table(u'crsq_articleinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100L, db_index=True)),
            ('articletitle', self.gf('django.db.models.fields.CharField')(max_length=100L)),
            ('articleimage', self.gf('django.db.models.fields.TextField')(max_length=100L)),
            ('articlecontent', self.gf('django.db.models.fields.TextField')()),
            ('twitterpower', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fbpower', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'crsq', ['ArticleInfo'])


    def backwards(self, orm):
        # Removing unique constraint on 'TwitterListLinks', fields ['sector', 'twitteruser', 'twitterlist', 'tweetid']
        db.delete_unique(u'crsq_twitterlistlinks', ['sector', 'twitteruser', 'twitterlist', 'tweetid'])

        # Removing unique constraint on 'TwitterKeywordLinks', fields ['keyword', 'tweetid']
        db.delete_unique(u'crsq_twitterkeywordlinks', ['keyword', 'tweetid'])

        # Removing unique constraint on 'TweetLinks', fields ['tweetid', 'url']
        db.delete_unique(u'crsq_tweetlinks', ['tweetid', 'url'])

        # Deleting model 'TweetLinks'
        db.delete_table(u'crsq_tweetlinks')

        # Deleting model 'TwitterKeywordLinks'
        db.delete_table(u'crsq_twitterkeywordlinks')

        # Deleting model 'TwitterListLinks'
        db.delete_table(u'crsq_twitterlistlinks')

        # Deleting model 'ArticleInfo'
        db.delete_table(u'crsq_articleinfo')


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
        u'crsq.tweetlinks': {
            'Meta': {'unique_together': "(('tweetid', 'url'),)", 'object_name': 'TweetLinks'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100L'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100L', 'null': 'True'}),
            'tweetid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'db_index': 'True'})
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