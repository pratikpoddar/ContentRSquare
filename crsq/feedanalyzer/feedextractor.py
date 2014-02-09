import feedparser
from bs4 import BeautifulSoup
from crsq.models import ArticleInfo
from crsq.crsqlib import urlutils
import datetime
import logging

logger = logging.getLogger(__name__)

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def load_rss_in_table(rss_url):
	feed = feedparser.parse(rss_url)
	for entry in feed['items']:
		put_article_details(entry)

	return
	
def put_article_details(entry):
	url = entry['feedburner_origlink']
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



load_rss_in_table("http://feeds.feedburner.com/TechCrunch/")



