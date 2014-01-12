from django.db import models
from datetime import datetime

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

class TwitterListLinks(models.Model):
    sector = models.CharField(max_length=100L, null=False)
    twitteruser = models.CharField(max_length=100L, null=False)
    twitterlist = models.CharField(max_length=100L, null=False)
    url = models.CharField(max_length=100L, null=False, db_index=True)
    tweetid = models.BigIntegerField(null=False, db_index=True)
    location = models.CharField(max_length=100L, default=None, null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        unique_together = (("sector", "twitteruser", "twitterlist", "url", "tweetid"),)

class TwitterKeywordLinks(models.Model):
    keyword = models.CharField(max_length=100L, null=False)
    url = models.CharField(max_length=100L, null=False, db_index=True)
    tweetid = models.BigIntegerField(null=False, db_index=True)
    location = models.CharField(max_length=100L, default=None, null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        unique_together = (("keyword", "url", "tweetid"),)

class ArticleInfo(models.Model):
    url = models.CharField(max_length=100L, null=False, db_index=True, unique=True)
    articletitle = models.CharField(max_length=100L)
    articleimage = models.TextField(max_length=100L)
    articlecontent = models.TextField()
    twitterpower = models.IntegerField(default=0)
    fbpower = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True, blank=True)




 
	

