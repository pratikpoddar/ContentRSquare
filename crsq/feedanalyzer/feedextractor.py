import feedparser
from bs4 import BeautifulSoup
from crsq.models import ArticleInfo, ArticleTags, ArticleSemantics
from crsq.crsqlib import urlutils, articleutils
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

def load_rss_in_table(rss_url):
	logger.debug('feedanalyzer - load_rss_in_table - ' + rss_url)
	try:
		rss_url = urlutils.getCanonicalUrl(rss_url)
		feed = feedparser.parse(rss_url)
		for entry in feed['items']:
			if 'feedburner_origlink' in entry.keys():
				put_article_details(entry)
				put_article_semantics_tags(urlutils.getCanonicalUrl(entry['feedburner_origlink']))
			elif 'link' in entry.keys():
				put_article_details(entry)
				put_article_semantics_tags(urlutils.getCanonicalUrl(entry['link']))
	except Exception as e:
		logger.exception('feedanalyzer - load_rss_in_table - error - ' + rss_url + ' - ' + str(e))
	return
	
def put_article_details(entry):
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

        	                articleinfo = ArticleInfo(url=urlutils.getCanonicalUrl(url), articletitle = crsq_unicode(entry['title']), articleimage = articleimage, articlecontent = crsq_unicode(BeautifulSoup(crsq_unicode(entry['content'][0]['value'])).text), articledate = articledate, articlehtml = crsq_unicode(entry['content'][0]['value']), twitterpower= socialpower['tw'], fbpower = socialpower['fb'])
				articleinfo.save()
	                except Exception as e:
        	                logger.exception('feedanalyzer - put_article_details - error saving article - ' + removeNonAscii(url) + ' - ' + str(e))
        return

def put_article_semantics_tags(url):
        url = urlutils.getCanonicalUrl(url)
        if ArticleInfo.objects.filter(url=url).count()==0:
                return
        if ArticleSemantics.objects.filter(url=url).count()==0 or ArticleTags.objects.filter(url=url).count()==0:
                try:
                        content = crsq_unicode(ArticleInfo.objects.filter(url=url).values('articlecontent')[0]['articlecontent'])
                        semantics_dict = articleutils.getArticleSemanticsTags(content)
                        semantics_row = ArticleSemantics(url=urlutils.getCanonicalUrl(url), summary = crsq_unicode(semantics_dict['summary']), topic = crsq_unicode(semantics_dict['topic']))
                        if ArticleSemantics.objects.filter(url=url).count()==0:
                                semantics_row.save()
                        if ArticleTags.objects.filter(url=url).count()==0:
                                for tag in semantics_dict['tags']:
                                        tag_row = ArticleTags(url=url, tag=crsq_unicode(tag))
                                        if ArticleTags.objects.filter(url=url, tag=crsq_unicode(tag)).count()==0:
                                                tag_row.save()
                except Exception as e:
                        logger.exception('feedanalyzer - put_article_semantics_tags - error getting article semantics / tags - ' + removeNonAscii(url) + ' - ' + str(e))

        return


