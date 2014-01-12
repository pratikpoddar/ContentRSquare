import tweepy
import json
import jsonpickle
from time import sleep
import sys
import itertools
from crsq.crsqlib import urlutils
import hashlib
from django.db.models import Max
import logging

from crsq.models import TwitterListLinks, TwitterKeywordLinks

logger = logging.getLogger(__name__)

consumer_key="nNRGguiHtC5AouxzUlZQ"
consumer_secret="T3df1h6SIqitUs50mlPlbrTN9JrEMZzZK9h6ChYCGw"
access_token="66690578-TeOd1CQGR6KaF3cQvyNE59XPLYLJ7HAmu2DLLqTri"
access_token_secret="rGJYuYUJiSnUEqP0wxDNpfNVidPxZFqkuKkGDu3i3jI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def search_twitter(keyword, numlinks):

	logger.debug('twitter_newspaper - search_twitter - called for ' + keyword)

        ## Create empty list of hold statuses
        status_list = []

        ## Get SinceId as the last tweetid in the sector / twitteruser / twitterlist
        try:
                theSinceId = TwitterKeywordLinks.objects.filter(keyword=keyword).aggregate(Max('tweetid'))['tweetid__max']
        except Exception as e:
                logger.exception('twitter_newspaper - search_twitter - getSinceId for ' + keyword + ' - ' + str(e))
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
                logger.exception('twitter_newspaper - search_twitter - error getting twitter statuses - ' + keyword + ' - ' + str(e))
                pass

        ## Processing the urls in the statuses and saving them
        for status in status_list:
		try:
	                urls = map(lambda x: urlutils.getCanonicalUrl(urlutils.getLongUrlOptimized(x['expanded_url'])), status.entities['urls'])
		except Exception as e:
			logger.exception('twitter_newspaper - search_twitter - error getting Long Urls ' + str(status.id) + ' ' + str(e))
			urls = []
                urls = filter(lambda x: urlutils.is_url_an_article(x), urls)
                for url in urls:
                        twitterlink = TwitterKeywordLinks(keyword=keyword, url=url, tweetid=status.id, location=status.author.location)
                        try:
                                twitterlink.save()
                        except Exception as e:
                                logger.exception('twitter_newspaper - search_twitter - error saving twitterlink - ' + keyword + ' ' + url + ' - ' + str(e))
                                pass

        return

def get_list_timeline(sector, twitteruser, twitterlist, numlinks):

	logger.debug('twitter_newspaper - get_list_timeline - called for ' + sector + ' ' + twitteruser + ' ' + twitterlist)

	## Create empty list of hold statuses
	status_list = []

	## Get SinceId as the last tweetid in the sector / twitteruser / twitterlist
	try:
		theSinceId = TwitterListLinks.objects.filter(sector=sector, twitteruser=twitteruser, twitterlist=twitterlist).aggregate(Max('tweetid'))['tweetid__max']
	except Exception as e:
		logger.exception('twitter_newspaper - get_list_timeline - getSinceId for ' + sector + ' ' + twitteruser + ' ' + twitterlist + ' - ' + str(e))
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
                logger.exception('twitter_newspaper - get_list_timeline - error getting twitter statuses - ' + sector + ' ' + twitteruser + ' ' + twitterlist + ' - ' + str(e))
		pass

	## Processing the urls in the statuses and saving them
	for status in status_list:
		try:
		        urls = map(lambda x: urlutils.getCanonicalUrl(urlutils.getLongUrlOptimized(x['expanded_url'])), status.entities['urls'])
		except Exception as e:
			logger.exception('twitter_newspaper - get_list_timeline - error getting Long Urls ' + str(status.id) + ' ' + str(e))
			urls = []
        	urls = filter(lambda x: urlutils.is_url_an_article(x), urls)
		for url in urls:
			twitterlink = TwitterListLinks(sector=sector, twitteruser=twitteruser, twitterlist=twitterlist, url=url, tweetid=status.id, location=status.author.location)
			try:
				twitterlink.save()
			except:
		                logger.exception('twitter_newspaper - get_list_timeline - error saving twitterlink - ' + sector + ' ' + twitteruser + ' ' + twitterlist + ' ' + url + ' - ' + str(e))
				pass

	return

#get_list_timeline("startups", "pratikpoddar", "startups", 100)
#search_twitter("sachin tendulkar", 100)


