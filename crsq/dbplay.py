from crsq.models import *
from crsq.crsqlib import urlutils
from crsq.crsqlib.text_summarize import text_summarize
from urlparse import urlparse
import pickle
from django.db.models import Count
from crsq.crsqlib.articleutils import *
import datetime

urls=[]
#urls = map(lambda x: x['url'], ArticleInfo.objects.filter(articledate__gt=datetime.date(2015,1,1)).values('url'))
print len(urls)
counter = 0
for url in urls:
	counter+=1
	try:
		print url
		print counter
		d1 = ArticleInfo.objects.get(url=url).articledate
		d2 = getArticlePropertiesFromUrl(url=url)['publish_date']
		if d2<datetime.date(2014,4,4):
			a = ArticleInfo.objects.get(url=url)
			a.articledate = d2
			a.save()
			print url
			print d1
			print ArticleInfo.objects.get(url=url).articledate
	except:
		pass

#url='http://www.cbssports.com/nfl/eye-on-football/24466743/anquan-boldin-no-rift-between-49ers-players-and-jim-harbaugh'
#h = ArticleInfo.objects.get(url=url).articlehtml
#getArticleProperties(h)['publish_date']

l11 = ArticleInfo.objects.filter(url__contains="/~r/") | ArticleInfo.objects.filter(url__contains="http://feed") | ArticleInfo.objects.filter(url__contains="glogin") | ArticleInfo.objects.filter(url__contains="feeds")
l11= map(lambda x: x['url'], l11.values('url'))
for url in l11:
	url2 = urlutils.getLongUrl(url)
	if url2 not in l11:
		articleutilsdb.put_article_details(url2)
		articleurilsdb.put_article_semantics_tags(url2)		




		
	


