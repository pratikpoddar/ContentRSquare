from crsq.models import *
from crsq.crsqlib import urlutils
from crsq.crsqlib.text_summarize import text_summarize
from urlparse import urlparse
import pickle
from django.db.models import Count
from crsq.crsqlib.articleutils import *
import datetime

urls = map(lambda x: x['url'], ArticleInfo.objects.filter(articledate__gt=datetime.date(2015,1,1)).values('url'))
print len(urls)
counter = 0
for url in urls:
	counter+=1
	try:
		print url
		print counter
		d1 = ArticleInfo.objects.get(url=url).articledate
		d2 = getArticleProperties(ArticleInfo.objects.get(url=url).articlehtml)['publish_date']
		if d2<datetime.date(2014,11,11):
			a = ArticleInfo.objects.get(url=url)
			a.articledate = d2
			a.save()
			print url
			print d1
			print ArticleInfo.objects.get(url=url).articledate
	except:
		pass

