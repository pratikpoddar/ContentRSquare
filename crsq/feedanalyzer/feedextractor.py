import feedparser
from bs4 import BeautifulSoup
from crsq.models import ArticleInfo, ArticleTags, ArticleSemantics
from crsq.crsqlib import urlutils, articleutils, articleutilsdb
import datetime
import logging
import json
import jsonpickle
import hashlib

logger = logging.getLogger(__name__)

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def crsq_unicode(s):

        if s  == None:
                return s

        if isinstance(s, unicode):
                return s
        else:
                return s.decode('utf-8')

def load_rss_in_table(rss_url, extractor):
	logger.debug('feedanalyzer - load_rss_in_table - ' + rss_url)
	try:
		rss_url = urlutils.getCanonicalUrl(rss_url)
		feed = feedparser.parse(rss_url)
		for entry in feed['items']:
			if 'content' in entry.keys() and 'title' in entry.keys():
				if 'feedburner_origlink' in entry.keys():
					url = urlutils.getCanonicalUrl(entry['feedburner_origlink'])
				elif 'link' in entry.keys():
					url = urlutils.getCanonicalUrl(entry['link'])

				if extractor=="feed":
					feedanalyzer_put_article_details(entry)
				if extractor=="fromscratch":
					articleutilsdb.put_article_details(urlutils.getCanonicalUrl(url), source="feedanalyzer"+extractor)

				if extractor in ["feed", "fromscratch"]:
					articleutilsdb.put_article_semantics_tags(urlutils.getCanonicalUrl(url))
	except Exception as e:
		logger.exception('feedanalyzer - load_rss_in_table - error - ' + rss_url + ' - ' + str(e))
	return
	
def feedanalyzer_put_article_details(entry):
	if 'feedburner_origlink' in entry.keys():
		url = urlutils.getCanonicalUrl(entry['feedburner_origlink'])
	elif 'link' in entry.keys():
		url = urlutils.getCanonicalUrl(entry['link'])
	
	url = urlutils.getCanonicalUrl(url)
	if url:
	        if ArticleInfo.objects.filter(url=url).count()==0:
        	        try:
                	        socialpower = urlutils.getSocialShares(url)
				try:
					d = entry['published_parsed']
					articledate = datetime.date(d[0], d[1], d[2])
				except:
					articledate = None

				try:
					articleimage = urlutils.getCanonicalUrl(entry['media_thumbnail'][0]['url'])
				except:
					articleimage = None

        	                articleinfo = ArticleInfo(url=urlutils.getCanonicalUrl(url), articletitle = crsq_unicode(entry['title']), articleimage = articleimage, articlecontent = crsq_unicode(BeautifulSoup(crsq_unicode(' '.join(map(lambda x: x['value'], entry['content'])))).text), articledate = articledate, articlehtml = crsq_unicode(BeautifulSoup(crsq_unicode(' '.join(map(lambda x: x['value'], entry['content'])))).text), twitterpower= socialpower['tw'], fbpower = socialpower['fb'], source='feedanalyzer')
				articleinfo.save()
	                except Exception as e:
        	                logger.exception('feedanalyzer - feedanalyzer_put_article_details - error saving article - ' + removeNonAscii(url) + ' - ' + str(e))
        return

