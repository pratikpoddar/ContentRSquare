import tweepy
import json
import jsonpickle
from time import sleep
import sys
import itertools
from crsq.crsqlib import urlutils, articleutils
import hashlib
from django.db.models import Max
import logging
from urlparse import urlparse
from crsq.crsqlib.articleutilsdb import put_article_details, put_article_semantics_tags
from crsq.models import TwitterListLinks, TwitterKeywordLinks, TweetLinks, TweetUsers, ArticleInfo, ArticleSemantics, ArticleTags
from functools32 import lru_cache

logger = logging.getLogger(__name__)

consumer_key="nNRGguiHtC5AouxzUlZQ"
consumer_secret="T3df1h6SIqitUs50mlPlbrTN9JrEMZzZK9h6ChYCGw"
access_token="66690578-TeOd1CQGR6KaF3cQvyNE59XPLYLJ7HAmu2DLLqTri"
access_token_secret="rGJYuYUJiSnUEqP0wxDNpfNVidPxZFqkuKkGDu3i3jI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

twitter_newspaper_blocked_domains = ['thehill.com', 'shortyawards.com', 'ciowhitepapers.com', 'docquery.fec.gov', 'zao.com', 'thereformedbroker.com', 'indiadigitalreview.com', 'jwatch.org', 'c-span.org', 'whitehouse.gov', 'uber.com', 'ritholtz.com', 'geekwire.com', 'online.wsj.com', 'guardianlv.com']

tw_np_sector_list = ["Technology", "Politics", "Entertainment", "Sports", "Business"]
tw_np_location_list = ["World", "United States", "India", "San Francisco, USA", "New York, USA", "Boston, USA", "London, UK", "Mumbai, India", "Bangalore, India"]

def tw_np_location_alias(location):

        location_alias = []

        if location == "world":
                location_alias = ["boston-usa", "san-francisco-usa", "new-york-usa", "mumbai-india", "bangalore-india", "london-uk"]
        if location == "united-states":
                location_alias = ["boston-usa", "san-francisco-usa", "new-york-usa"]
        if location == "india":
                location_alias = ["mumbai-india", "bangalore-india"]
        if location == "san-francisco-usa":
                location_alias = [location]
        if location == "new-york-usa":
                location_alias = [location]
        if location == "boston-usa":
                location_alias = [location]
        if location == "london-uk":
                location_alias = [location]
        if location == "mumbai-india":
                location_alias = [location]
        if location == "bangalore-india":
                location_alias = [location]
	
	return location_alias

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def search_twitter(keyword, numlinks):

	logger.debug('twitter_newspaper - search_twitter - called for ' + keyword)

        ## Create empty list of hold statuses
        status_list = []

        ## Get SinceId as the last tweetid in the keyword
        try:
                theSinceId = TwitterKeywordLinks.objects.filter(keyword=keyword).aggregate(Max('tweetid'))['tweetid__max']
        except Exception as e:
                logger.exception('twitter_newspaper - search_twitter - getSinceId for ' + removeNonAscii(keyword) + ' - ' + str(e))
                theSinceId = None

        ## Get all the statuses
        try:
	        for tweet in tweepy.Cursor(api.search,
                	        q=keyword+" filter:news",
	                        rpp=100,
	                        result_type="recent",
	                        include_entities=True,
	                        geocode="",
	                        lang="en").items():
	       	        status_list.append(tweet)
        	        if len(status_list)>numlinks:
                	        break
	                if tweet.id <= theSinceId:
        	                break

        except Exception as e:
                logger.exception('twitter_newspaper - search_twitter - error getting twitter statuses - ' + removeNonAscii(keyword) + ' - ' + str(e))
                raise

        ## Processing the urls in the statuses and saving them
	for status in status_list:
		try:
                        urls = map(lambda x: x['expanded_url'], status.entities['urls'])
                        urls = filter(lambda x: urlutils.is_url_an_article(x), urls)
                        urls = filter(lambda x: x.find('@') < 0, urls)
                        urls = filter(lambda x: urlparse(x)[1].replace('www.','') not in twitter_newspaper_blocked_domains, urls)
                        urls = map(lambda x: urlutils.getCanonicalUrl(urlutils.getLongUrlOptimized(x)), urls)
		except Exception as e:
			logger.exception('twitter_newspaper - search_twitter - error getting Long Urls ' + str(status.id) + ' ' + str(e))
			urls = []
		urls = filter(lambda x: urlutils.is_url_an_article(x), urls)
		urls = filter(lambda x: x.find('@') < 0, urls)
                urls = filter(lambda x: urlparse(x)[1].replace('www.','') not in twitter_newspaper_blocked_domains, urls)
		twitterkeywordlink = TwitterKeywordLinks(keyword=keyword, tweetid=status.id)
		if TweetLinks.objects.filter(tweetid=status.id).count() == 0:
			for url in urls:
				twitterlink = TweetLinks(tweetid=status.id, author=status.author.screen_name, url=url)
				try:
					twitterlink.save()
				except Exception as e:
					logger.exception('twitter_newspaper - search_twitter - error saving twitterlink - ' + removeNonAscii(keyword) + ' ' + url + ' - ' + str(e))
                	                pass
		try:
			twitterkeywordlink.save()
		except Exception as e:
			logger.exception('twitter_newspaper - search_twitter - error saving twitterkeywordlink - ' + removeNonAscii(keyword) + ' - ' + str(e))


        return

def get_list_timeline(twitteruser, twitterlist, numlinks):

	logger.debug('twitter_newspaper - get_list_timeline - called for ' + twitteruser + ' ' + twitterlist)

	## Create empty list of hold statuses
	status_list = []

	## Get SinceId as the last tweetid in the twitteruser / twitterlist
	try:
		theSinceId = TwitterListLinks.objects.filter(twitteruser=twitteruser, twitterlist=twitterlist).aggregate(Max('tweetid'))['tweetid__max']
	except Exception as e:
		logger.exception('twitter_newspaper - get_list_timeline - getSinceId for ' + twitteruser + ' ' + twitterlist + ' - ' + str(e))
		theSinceId = None
	
	## Get all the statuses
	try:
		statuses = api.list_timeline(count=50, owner_screen_name=twitteruser, slug=twitterlist, include_entities="1", since_id=theSinceId)
		while (statuses != []) and (len(status_list)<numlinks):
		    for status in statuses:
			status_list.append(status)
		    
		    # Get tweet id from last status in each page
		    theMaxId = statuses[-1].id
		    theMaxId = theMaxId - 1

		    statuses = api.list_timeline(count=50, owner_screen_name=twitteruser, slug=twitterlist, include_entities="1", max_id=theMaxId, since_id=theSinceId)
	except Exception as e:
                logger.exception('twitter_newspaper - get_list_timeline - error getting twitter statuses - ' + twitteruser + ' ' + twitterlist + ' - ' + str(e))
		raise

	## Processing the urls in the statuses and saving them
	for status in status_list:
		try:
			urls = map(lambda x: x['expanded_url'], status.entities['urls'])
			urls = filter(lambda x: urlutils.is_url_an_article(x), urls)
			urls = filter(lambda x: x.find('@') < 0, urls)
			urls = filter(lambda x: urlparse(x)[1].replace('www.','') not in twitter_newspaper_blocked_domains, urls)
		        urls = map(lambda x: urlutils.getCanonicalUrl(urlutils.getLongUrlOptimized(x)), urls)
		except Exception as e:
			logger.exception('twitter_newspaper - get_list_timeline - error getting Long Urls ' + str(status.id) + ' ' + str(e))
			urls = []
        	urls = filter(lambda x: urlutils.is_url_an_article(x), urls)
		urls = filter(lambda x: x.find('@') < 0, urls)
		urls = filter(lambda x: urlparse(x)[1].replace('www.','') not in twitter_newspaper_blocked_domains, urls)
                twitterlistlink = TwitterListLinks(twitteruser=twitteruser, twitterlist=twitterlist, tweetid=status.id)
		if TweetLinks.objects.filter(tweetid=status.id).count() == 0:
			for url in urls:
				twitterlink = TweetLinks(tweetid=status.id, author=status.author.screen_name, url=url)
				try:
        	                        twitterlink.save()
	                        except Exception as e:
        	                        logger.exception('twitter_newspaper - get_list_timeline - error saving twitterlink - ' + str(status.id) + ' ' + url + ' - ' + str(e))
                	                pass
                try:
                        twitterlistlink.save()
                except Exception as e:
			logger.exception('twitter_newspaper - get_list_timeline - error saving twitterlistlink - ' + str(status.id) + ' - ' + str(e))


	return

@lru_cache(maxsize=1024)
def get_articles(sector, location, cursor=0):
	
	authors = map(lambda x: x['author'], TweetUsers.objects.filter(sector=sector, location__in=tw_np_location_alias(location)).values('author'))
	urls = map(lambda x: x['url'], TweetLinks.objects.filter(author__in=authors).values('url'))
	articles = ArticleInfo.objects.filter(url__in=urls).exclude(articleimage=None).order_by('-id')[cursor:cursor+10].values()
	return articles

def get_sharers(url):
	return TweetLinks.objects.filter(url=url).values('author', 'tweetid')


#get_list_timeline("pratikpoddar", "startups", 100)
#search_twitter("sachin tendulkar", 100)


