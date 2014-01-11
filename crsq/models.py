from django.db import models
from datetime import datetime
from picklefield.fields import PickledObjectField

class ContentAffiliate(models.Model):
    contenthash = models.BigIntegerField(unique=True, db_index=True, null=False)
    affiliate = PickledObjectField()
    content = models.CharField(max_length=100L, null=True)
    time= models.DateTimeField(auto_now_add=True, blank=True)

class AmazonProd(models.Model):
    text = models.CharField(max_length=100L, db_index=True, null=False)
    index = models.CharField(max_length=100L, null=False)
    amazonlink = models.CharField(max_length=100L, null=False)
    time= models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        unique_together = (("text", "index"),)

