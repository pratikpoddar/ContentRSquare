import feedparser
from bs4 import BeautifulSoup
from crsq.models import ArticleInfo, ArticleTags, ArticleSemantics
from crsq.crsqlib import urlutils, articleutils, articleutilsdb
import datetime
import logging
import json
import jsonpickle
import hashlib
from urlparse import urlparse

logger = logging.getLogger(__name__)

feedanalyzer_blocked_domains= ['guardianlv.com']

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def crsq_unicode(s):

        if s  == None:
                return s

        if isinstance(s, unicode):
                return s
        else:
                return s.decode('utf-8')

def pick_appropriate_url(entry):
	url = ""

	if 'link' in entry.keys():
        	urlcheck = urlutils.getCanonicalUrl(entry['link'])
		if (urlcheck.find('feeds.')==-1) and (urlcheck.find('feedburner.')==-1) and (urlcheck.find('feedproxy.')==-1) and (urlcheck.find('feedsportal.')==-1):
			url = urlcheck
			return url
			
	if 'feedburner_origlink' in entry.keys():
		urlcheck = urlutils.getCanonicalUrl(entry['feedburner_origlink'])
                if (urlcheck.find('feeds.')==-1) and (urlcheck.find('feedburner.')==-1) and (urlcheck.find('feedproxy.')==-1) and (urlcheck.find('feedsportal.')==-1):
			url = urlcheck
			return url

        if 'id' in entry.keys():
		try:
	                urlcheck = urlutils.getCanonicalUrl(entry['id'])
        	        if (urlcheck.find('feeds.')==-1) and (urlcheck.find('feedburner.')==-1) and (urlcheck.find('feedproxy.')==-1) and (urlcheck.find('feedsportal.')==-1):
                	        url = urlcheck
	                        return url
		except:
			pass

	if 'link' in entry.keys():
		return urlutils.getCanonicalUrl(entry['link'])

	if 'feedburner_origlink' in entry.keys():
		return urlutils.getCanonicalUrl(entry['feedburner_origlink'])
		
	return None	
	
def load_rss_in_table(rss_url, extractor):
	logger.debug('feedanalyzer - load_rss_in_table - ' + rss_url)
	try:
		rss_url = urlutils.getCanonicalUrl(rss_url)
		feed = feedparser.parse(rss_url)
		for entry in feed['items']:
			url = pick_appropriate_url(entry)
			if urlutils.is_url_an_article(url):
				if extractor=="feed":
					if 'content' in entry.keys() and 'title' in entry.keys():
						feedanalyzer_put_article_details(entry)
					else:
	                        	        articleutilsdb.put_article_details(urlutils.getCanonicalUrl(url), source="feedanalyzer"+extractor)

				if extractor=="fromscratch":
					articleutilsdb.put_article_details(urlutils.getCanonicalUrl(url), source="feedanalyzer"+extractor)

				articleutilsdb.put_article_semantics_tags(urlutils.getCanonicalUrl(url))

	except Exception as e:
		logger.exception('feedanalyzer - load_rss_in_table - error - ' + rss_url + ' - ' + str(e))
	return
	
def feedanalyzer_put_article_details(entry):

	url = pick_appropriate_url(entry)
	url = urlutils.getCanonicalUrl(url)
	if url:
	        if (ArticleInfo.objects.filter(url=url).count()==0) and (urlutils.is_url_an_article(url)) and ((urlparse(url)[1]) not in feedanalyzer_blocked_domains):
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

