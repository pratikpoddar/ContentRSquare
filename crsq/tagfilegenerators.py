from crsq.models import *
from crsq.crsqlib import urlutils
from crsq.crsqlib.text_summarize import text_summarize
from urlparse import urlparse
import pickle
from django.db.models import Count

"""
toptagshelp = map(lambda x: x['tag'], ArticleTags.objects.values('tag').annotate(Count('url')).order_by('-url__count')[:500])
toptags = []
for t in toptagshelp:
	fm = text_summarize.get_Freebase_Meaning(t.replace('-',' '))
	try:
		if fm['wikilink']:
			toptags.append(t)
	except:
		pass
toptags = list(set(toptags))
ImportantTags.objects.filter(source="top_tag").delete()
for tag in toptags:
	if ImportantTags.objects.filter(tag=tag, source="top_tag").count()==0:
		imptag = ImportantTags(tag=tag, source="top_tag")
	        imptag.save()

allurls = list(set(map(lambda x: x['url'], ArticleInfo.objects.exclude(articlecontent=None).exclude(articlecontent='').exclude(articleimage='').exclude(articleimage=None).values('url'))))
alltags = list(set(map(lambda x: x['tag'], ArticleTags.objects.filter(url__in=allurls).values('tag'))))
"""
from crsq.google_trends.gt import *
google_trends = get_all_google_trends()
def check_if_googlesearch_is_a_tag(googlesearch):
	if len(ArticleTags.objects.filter(tag=googlesearch).values('url'))>3:
		return googlesearch
	
	try:
		freebase_meaning = text_summarize.get_Freebase_Meaning(googlesearch.replace('-',' '))
		if freebase_meaning['wikilink']:
			if len(ArticleTags.objects.filter(tag=slugify(freebase_meaning['title'])).values('url'))>3:
				return slugify(freebase_meaning['title']) 
	except:
		pass

	return None

#google_trends = {k: filter(lambda y: y, list(set(map(lambda x: check_if_googlesearch_is_a_tag(x), v)))) for k, v in google_trends.items()}
tagfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/googletrendstags.txt', 'w')
pickle.dump(google_trends, tagfile)
tagfile.close()


for country in google_trends.keys():
	for tag in google_trends[country]:
		if ImportantTags.objects.filter(tag=tag, source="google_trend:"+country).count()==0:
		        imptag = ImportantTags(tag=tag, source="google_trend:"+country)
		        imptag.save()

