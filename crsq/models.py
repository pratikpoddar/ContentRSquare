from django.db import models
from datetime import datetime
from urlparse import urlparse

class ContentAffiliate(models.Model):
    contenthash = models.CharField(max_length=100L, unique=True, db_index=True, null=False)
    affiliate = models.TextField(null=False)
    content = models.CharField(max_length=100L, null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)

class AmazonProd(models.Model):
    text = models.CharField(max_length=100L, db_index=True, null=False)
    index = models.CharField(max_length=100L, null=False)
    amazonlink = models.CharField(max_length=100L, null=False)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        unique_together = (("text", "index"),)

class TweetLinks(models.Model):
    author = models.CharField(max_length=100L, null=False, db_index=True)
    tweetid = models.BigIntegerField(null=False, db_index=True)
    url = models.CharField(max_length=255L, null=False, db_index=True)
    class Meta:
        unique_together = (("tweetid", "url"),)

class TweetUsers(models.Model):
    sector = models.CharField(max_length=100L, null=False, db_index=True)
    location = models.CharField(max_length=100L, null=False, db_index=True)
    author = models.CharField(max_length=100L, null=False, db_index=True)

class TwitterListLinks(models.Model):
    twitteruser = models.CharField(max_length=100L, null=False)
    twitterlist = models.CharField(max_length=100L, null=False)
    tweetid = models.BigIntegerField(null=False, db_index=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        unique_together = (("sector", "twitteruser", "twitterlist", "tweetid"),)

class TwitterKeywordLinks(models.Model):
    keyword = models.CharField(max_length=100L, null=False)
    tweetid = models.BigIntegerField(null=False, db_index=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        unique_together = (("keyword", "tweetid"),)

class ArticleInfo(models.Model):
    url = models.CharField(max_length=255L, null=False, db_index=True, unique=True)
    articletitle = models.CharField(max_length=1000L)
    articleimage = models.TextField(max_length=1000L, null=True, default=None)
    articlecontent = models.TextField()
    articlehtml = models.TextField()
    articledate = models.DateField(null=True)
    twitterpower = models.IntegerField(default=0)
    fbpower = models.IntegerField(default=0)
    source = models.CharField(max_length=300L, null=True, blank=True, default=None)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    def domainname(self):
        return urlparse(self.url)[1]

class ArticleSemantics(models.Model):
    url = models.CharField(max_length=255L, null=False, db_index=True, unique=True)
    summary = models.TextField()
    topic = models.CharField(max_length=1000L, null=True, default=None)
    time = models.DateTimeField(auto_now_add=True, blank=True)

class ArticleTags(models.Model):
    url = models.CharField(max_length=255L, null=False, db_index=True)
    tag = models.CharField(max_length=255L, null=False, db_index=True)
    class Meta:
        unique_together = (("url", "tag"),)

class ImportantTags(models.Model):
    tag = models.CharField(max_length=255L, null=False)
    source = models.CharField(max_length=255L, null=False)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    
class PenPatronUser(models.Model):
    name = models.CharField(max_length=255L, null=False)
    email = models.CharField(max_length=255L, null=False)
    phone = models.CharField(max_length=255L, null=False)
    college = models.CharField(max_length=1000L, null=False)
    blog = models.CharField(max_length=1000L, null=False)
    message = models.CharField(max_length=1000L, null=False)
    time = models.DateTimeField(auto_now_add=True, blank=True)





 
	

