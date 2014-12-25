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
import langid
import re
from crsq.crsqlib.stringutils import *
from crsq.crsqlib.twitter_posting import post_twitter_crsq
from django.template.defaultfilters import slugify

langid.langid.load_model()

logger = logging.getLogger(__name__)

langid_identifier = langid.langid.identifier

feedanalyzer_blocked_domains= ['guardianlv.com']

def pick_appropriate_url(entry):
	url = ""

	if 'link' in entry.keys():
        	urlcheck = urlutils.getCanonicalUrl(entry['link'])
		if (urlcheck.find('feeds.')==-1) and (urlcheck.find('feedburner.')==-1) and (urlcheck.find('feedproxy.')==-1) and (urlcheck.find('feedsportal.')==-1):
			url = urlcheck
			if urlparse(url)[0]:
				return url
			
	if 'feedburner_origlink' in entry.keys():
		urlcheck = urlutils.getCanonicalUrl(entry['feedburner_origlink'])
                if (urlcheck.find('feeds.')==-1) and (urlcheck.find('feedburner.')==-1) and (urlcheck.find('feedproxy.')==-1) and (urlcheck.find('feedsportal.')==-1):
			url = urlcheck
                        if urlparse(url)[0]:
                                return url

        if 'id' in entry.keys():
		try:
	                urlcheck = urlutils.getCanonicalUrl(entry['id'])
        	        if (urlcheck.find('feeds.')==-1) and (urlcheck.find('feedburner.')==-1) and (urlcheck.find('feedproxy.')==-1) and (urlcheck.find('feedsportal.')==-1):
                	        url = urlcheck
	                        if urlparse(url)[0]:
        	                        return url
		except:
			pass

	if 'link' in entry.keys():
		url = urlutils.getCanonicalUrl(entry['link'])
		if urlparse(url)[0]:
                	return url

	if 'feedburner_origlink' in entry.keys():
		url = urlutils.getCanonicalUrl(entry['feedburner_origlink'])
                if urlparse(url)[0]:
                        return url
		
	return None	
	
def load_rss_in_table(rss_url, extractor):
	
	logger.debug('feedanalyzer - load_rss_in_table - ' + rss_url)
	try:
		rss_url = urlutils.getCanonicalUrl(rss_url)
		feed = feedparser.parse(rss_url)
		for entry in feed['items']:
			url = pick_appropriate_url(entry)
			if urlutils.is_url_an_article(url):
				url = urlutils.getCanonicalUrl(url)
				if urlutils.is_url_an_article(url):
					posted_before = ArticleInfo.objects.filter(url=url).count()
					if extractor=="feed":
						if 'content' in entry.keys() and 'title' in entry.keys():
							feedanalyzer_put_article_details(entry, rss_url)
						else:
		                        	        articleutilsdb.put_article_details(url, source="feedanalyzer"+extractor+rss_url)

					if extractor=="fromscratch":
						url = urlutils.getLongUrl(url)
						articleutilsdb.put_article_details(url, source="feedanalyzer"+extractor+rss_url)

					articleutilsdb.put_article_semantics_tags(url)
					try:
						if not posted_before:
							title = ArticleInfo.objects.get(url=url).articletitle
							tags = map(lambda x: x['tag'], ArticleTags.objects.filter(url=url).values('tag'))
							znlink = "http://www.zippednews.com/"+slugify(sorted(filter(lambda x: x.lower().replace('-',' ') in title.lower(), tags), key=lambda x: -len(x))[0])
							post_twitter_crsq(znlink, url, title, tags)
					except:
						pass
	except Exception as e:
		logger.exception('feedanalyzer - load_rss_in_table - error - ' + rss_url + ' - ' + str(e))
	return
	
def feedanalyzer_put_article_details(entry, rss_url):

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

        	                articleinfo = ArticleInfo(url=urlutils.getCanonicalUrl(url), articletitle = crsq_unicode(entry['title']), articleimage = articleimage, articlecontent = crsq_unicode(BeautifulSoup(crsq_unicode(' '.join(map(lambda x: x['value'], entry['content'])))).text), articledate = articledate, articlehtml = crsq_unicode(BeautifulSoup(crsq_unicode(' '.join(map(lambda x: x['value'], entry['content'])))).text), twitterpower= socialpower['tw'], fbpower = socialpower['fb'], source='feedanalyzer' + rss_url)
				if len(crsq_unicode(BeautifulSoup(crsq_unicode(' '.join(map(lambda x: x['value'], entry['content'])))).text))>250:
					if ArticleInfo.objects.filter(contenthash=str(int(hashlib.md5(removeNonAscii(crsq_unicode(BeautifulSoup(crsq_unicode(' '.join(map(lambda x: x['value'], entry['content'])))).text))).hexdigest(), 16))).count()==0:
						try:
							if langid_identifier.classify( re.match(r'(?:[^.:]*[.:]){2}', removeNonAscii(crsq_unicode(BeautifulSoup(crsq_unicode(' '.join(map(lambda x: x['value'], entry['content'])))).text))).group())[0]=='en':
								articleinfo.save()
						except:
							articleinfo.save()
	                except Exception as e:
        	                logger.exception('feedanalyzer - feedanalyzer_put_article_details - error saving article - ' + removeNonAscii(url) + ' - ' + str(e))
        return

