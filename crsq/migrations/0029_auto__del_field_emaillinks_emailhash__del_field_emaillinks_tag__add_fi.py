# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'EmailTags', fields ['emailhash', 'tag']
        db.delete_unique(u'crsq_emailtags', ['emailhash', 'tag'])

        # Removing unique constraint on 'EmailLinks', fields ['emailhash', 'tag']
        db.delete_unique(u'crsq_emaillinks', ['emailhash', 'tag'])

        # Deleting field 'EmailLinks.emailhash'
        db.delete_column(u'crsq_emaillinks', 'emailhash')

        # Deleting field 'EmailLinks.tag'
        db.delete_column(u'crsq_emaillinks', 'tag')

        # Adding field 'EmailLinks.messageid'
        db.add_column(u'crsq_emaillinks', 'messageid',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255L, db_index=True),
                      keep_default=False)

        # Adding field 'EmailLinks.link'
        db.add_column(u'crsq_emaillinks', 'link',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255L, db_index=True),
                      keep_default=False)

        # Adding unique constraint on 'EmailLinks', fields ['messageid', 'link']
        db.create_unique(u'crsq_emaillinks', ['messageid', 'link'])

        # Deleting field 'EmailTags.emailhash'
        db.delete_column(u'crsq_emailtags', 'emailhash')

        # Adding field 'EmailTags.messageid'
        db.add_column(u'crsq_emailtags', 'messageid',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255L, db_index=True),
                      keep_default=False)

        # Adding unique constraint on 'EmailTags', fields ['messageid', 'tag']
        db.create_unique(u'crsq_emailtags', ['messageid', 'tag'])


    def backwards(self, orm):
        # Removing unique constraint on 'EmailTags', fields ['messageid', 'tag']
        db.delete_unique(u'crsq_emailtags', ['messageid', 'tag'])

        # Removing unique constraint on 'EmailLinks', fields ['messageid', 'link']
        db.delete_unique(u'crsq_emaillinks', ['messageid', 'link'])

        # Adding field 'EmailLinks.emailhash'
        db.add_column(u'crsq_emaillinks', 'emailhash',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255L, db_index=True),
                      keep_default=False)

        # Adding field 'EmailLinks.tag'
        db.add_column(u'crsq_emaillinks', 'tag',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255L, db_index=True),
                      keep_default=False)

        # Deleting field 'EmailLinks.messageid'
        db.delete_column(u'crsq_emaillinks', 'messageid')

        # Deleting field 'EmailLinks.link'
        db.delete_column(u'crsq_emaillinks', 'link')

        # Adding unique constraint on 'EmailLinks', fields ['emailhash', 'tag']
        db.create_unique(u'crsq_emaillinks', ['emailhash', 'tag'])

        # Adding field 'EmailTags.emailhash'
        db.add_column(u'crsq_emailtags', 'emailhash',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255L, db_index=True),
                      keep_default=False)

        # Deleting field 'EmailTags.messageid'
        db.delete_column(u'crsq_emailtags', 'messageid')

        # Adding unique constraint on 'EmailTags', fields ['emailhash', 'tag']
        db.create_unique(u'crsq_emailtags', ['emailhash', 'tag'])


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
            'articledate': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'}),
            'articlehtml': ('django.db.models.fields.TextField', [], {}),
            'articleimage': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1000L', 'null': 'True'}),
            'articletitle': ('django.db.models.fields.CharField', [], {'max_length': '1000L'}),
            'contenthash': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255L', 'db_index': 'True'}),
            'contentlength': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'db_index': 'True'}),
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
        u'crsq.emailinfo': {
            'Meta': {'unique_together': "(('user', 'messageid'),)", 'object_name': 'EmailInfo'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'cleanbody': ('django.db.models.fields.TextField', [], {}),
            'emailbccto': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255L', 'null': 'True', 'blank': 'True'}),
            'emailccto': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255L', 'null': 'True', 'blank': 'True'}),
            'emailfrom': ('django.db.models.fields.CharField', [], {'max_length': '255L'}),
            'emailhash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_index': 'True'}),
            'emailtime': ('django.db.models.fields.DateTimeField', [], {}),
            'emailto': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255L', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messageid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_index': 'True'}),
            'shortbody': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000L'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255L'})
        },
        u'crsq.emaillinks': {
            'Meta': {'unique_together': "(('messageid', 'link'),)", 'object_name': 'EmailLinks'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_index': 'True'}),
            'messageid': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_index': 'True'})
        },
        u'crsq.emailtags': {
            'Meta': {'unique_together': "(('messageid', 'tag'),)", 'object_name': 'EmailTags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messageid': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_index': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_index': 'True'})
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