from crsq.models import *
from functools32 import lru_cache
from crsq.crsqlib import article_elastic_search
from crsq.crsqlib import imageutils

maxid = ArticleInfo.objects.all().order_by("-id")[0].id
ai = ArticleInfo.objects.filter(id__gt=maxid-400)

@lru_cache(maxsize=1024)
def getRelevantTags():

        relevanttags = sorted(filter(lambda x: len(x)<20, list(set(map(lambda x: x['tag'], ImportantTags.objects.all().values('tag'))))))

	return relevanttags

@lru_cache(maxsize=1024)
def getAppropriateImageTag(tag):

	searchterm = tag.replace('-',' ').title()
	searchterm2 = '"' + searchterm + '"'
        urls = article_elastic_search.searchdoc(searchterm2, 10)
	if len(urls)==0:
		urls = article_elastic_search.searchdoc(searchterm, 10)
	images = filter(lambda y: y, map(lambda x: x['articleimage'], ArticleInfo.objects.filter(url__in=urls).values('articleimage')))

	for x in images:
		imsize = imageutils.imagesize(x) 
		if sum(imsize, 0) > 550:
			if imsize[1]>200:
				if len(filter(lambda y: x.find(y)>=0, ['mobiletor']))==0:
					return x
	return ""

@lru_cache(maxsize=1024)
def getAppropriateImageTopic(topic):
	
	bi = filter(lambda x: (x['source'].find('feedanalyzerfromscratchhttps://news.google.com/')>=0) and (x['source'].endswith('topic='+topic)), filter(lambda y: y['source'], ai.values('url', 'source', 'articleimage')))
	images = filter(lambda y: y, map(lambda x: x['articleimage'], bi))

	for x in images: 
		imsize = imageutils.imagesize(x)
		if sum(imsize, 0) > 550:
			if imsize[1]>200:
				return x
	
	return ""
	




