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

def load_rss_in_table(rss_url):
	logger.debug('feedanalyzer - load_rss_in_table - ' + rss_url)
	try:
		rss_url = urlutils.getCanonicalUrl(rss_url)
		feed = feedparser.parse(rss_url)
		for entry in feed['items']:
			if 'feedburner_origlink' in entry.keys():
				put_article_details(entry)
				put_article_semantics_tags(entry['feedburner_origlink'])
			if 'link' in entry.keys():
				put_article_details(entry)
				put_article_semantics_tags(entry['link'])
	except Exception as e:
		logger.exception('feedanalyzer - load_rss_in_table - error - ' + rss_url + ' - ' + str(e))
	return
	
def put_article_details(entry):
	if 'feedburner_origlink' in entry.keys():
		url = entry['feedburner_origlink']
	if 'link' in entry.keys():
		url = entry['link']
	
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
					articleimage = entry['media_thumbnail'][0]['url']
				except:
					articleimage = None

        	                articleinfo = ArticleInfo(url=url, articletitle = entry['title'], articleimage = articleimage, articlecontent = BeautifulSoup(removeNonAscii(entry['content'][0]['value'])).text, articledate = articledate, articlehtml = removeNonAscii(entry['content'][0]['value']), twitterpower= socialpower['tw'], fbpower = socialpower['fb'])
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
                        content = ArticleInfo.objects.filter(url=url).values('articlecontent')[0]['articlecontent']
                        semantics_dict = articleutils.getArticleSemanticsTags(content)
                        semantics_row = ArticleSemantics(url=url, summary = semantics_dict['summary'], topic = semantics_dict['topic'])
                        if ArticleSemantics.objects.filter(url=url).count()==0:
                                semantics_row.save()
                        if ArticleTags.objects.filter(url=url).count()==0:
                                for tag in semantics_dict['tags']:
                                        tag_row = ArticleTags(url=url, tag=tag)
                                        if ArticleTags.objects.filter(url=url, tag=tag).count()==0:
                                                tag_row.save()
                except Exception as e:
                        logger.exception('feedanalyzer - put_article_semantics_tags - error getting article semantics / tags - ' + removeNonAscii(url) + ' - ' + str(e))

        return


