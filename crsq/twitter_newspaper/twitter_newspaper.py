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

from crsq.models import TwitterListLinks, TwitterKeywordLinks, TweetLinks, ArticleInfo, ArticleSemantics, ArticleTags

logger = logging.getLogger(__name__)

consumer_key="nNRGguiHtC5AouxzUlZQ"
consumer_secret="T3df1h6SIqitUs50mlPlbrTN9JrEMZzZK9h6ChYCGw"
access_token="66690578-TeOd1CQGR6KaF3cQvyNE59XPLYLJ7HAmu2DLLqTri"
access_token_secret="rGJYuYUJiSnUEqP0wxDNpfNVidPxZFqkuKkGDu3i3jI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

twitter_newspaper_blocked_domains = ['thehill.com', 'shortyawards.com', 'ciowhitepapers.com', 'docquery.fec.gov', 'zao.com']

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
                raise

        ## Processing the urls in the statuses and saving them
	for status in status_list:
		try:
			urls = map(lambda x: urlutils.getCanonicalUrl(urlutils.getLongUrlOptimized(x['expanded_url'])), status.entities['urls'])
		except Exception as e:
			logger.exception('twitter_newspaper - search_twitter - error getting Long Urls ' + str(status.id) + ' ' + str(e))
			urls = []
		urls = filter(lambda x: urlutils.is_url_an_article(x), urls)
		urls = filter(lambda x: x.find('@') < 0, urls)
                urls = filter(lambda x: urlparse(x)[1].replace('www.','') not in twitter_newspaper_blocked_domains, urls)
		twitterkeywordlink = TwitterKeywordLinks(keyword=keyword, tweetid=status.id)
		if TweetLinks.objects.filter(tweetid=status.id).count() == 0:
			for url in urls:
				twitterlink = TweetLinks(tweetid=status.id, location=status.author.location, author=status.author.screen_name, url=url)
				try:
					twitterlink.save()
				except Exception as e:
					logger.exception('twitter_newspaper - search_twitter - error saving twitterlink - ' + keyword + ' ' + url + ' - ' + str(e))
                	                pass
		try:
			twitterkeywordlink.save()
		except Exception as e:
			logger.exception('twitter_newspaper - search_twitter - error saving twitterkeywordlink - ' + keyword + ' - ' + str(e))


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
		raise

	## Processing the urls in the statuses and saving them
	for status in status_list:
		try:
		        urls = map(lambda x: urlutils.getCanonicalUrl(urlutils.getLongUrlOptimized(x['expanded_url'])), status.entities['urls'])
		except Exception as e:
			logger.exception('twitter_newspaper - get_list_timeline - error getting Long Urls ' + str(status.id) + ' ' + str(e))
			urls = []
        	urls = filter(lambda x: urlutils.is_url_an_article(x), urls)
		urls = filter(lambda x: x.find('@') < 0, urls)
		urls = filter(lambda x: urlparse(x)[1].replace('www.','') not in twitter_newspaper_blocked_domains, urls)
                twitterlistlink = TwitterListLinks(sector=sector, twitteruser=twitteruser, twitterlist=twitterlist, tweetid=status.id)
		if TweetLinks.objects.filter(tweetid=status.id).count() == 0:
	                for url in urls:
        	                twitterlink = TweetLinks(tweetid=status.id, location=status.author.location, author=status.author.screen_name, url=url)
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

def put_article_details(url):
	if ArticleInfo.objects.filter(url=url).count()==0:
		try:
			articledict = articleutils.getArticlePropertiesFromUrl(url)
			socialpower = urlutils.getSocialShares(url)
			articleinfo = ArticleInfo(url=url, articletitle = articledict['title'], articleimage = articledict['image'], articlecontent = articledict['cleaned_text'], articledate = articledict['publish_date'], twitterpower= socialpower['tw'], fbpower = socialpower['fb'])
			if len(articledict['cleaned_text'].strip())>1:
				articleinfo.save()
		except Exception as e:
			logger.exception('twitter_newspaper - put_article_details - error saving article - ' + url + ' - ' + str(e))
	return

def put_article_semantics_tags(url):
	if ArticleInfo.objects.filter(url=url).count()==0:
		#logger.exception('twitter_newspaper - put_article_semantics_tags - error getting article content - ' + url + ' - ' + 'No content in ArticleInfo')
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
			logger.exception('twitter_newspaper - put_article_semantics_tags - error getting article semantics / tags - ' + url + ' - ' + str(e))

	return

def get_articles(sector, location):
	tweets = map(lambda x: x['tweetid'], TwitterListLinks.objects.filter(sector=sector).values('tweetid'))
	urls = map(lambda x: x['url'], TweetLinks.objects.filter(tweetid__in=tweets, location__contains='').values('url'))
	articles = ArticleInfo.objects.filter(url__in=urls).exclude(articleimage=None).order_by('-time').values()
	return filter(lambda x: len(x['articlecontent'])>300, articles)


def get_sharers(url):
	return TweetLinks.objects.filter(url=url).values('author', 'tweetid')


#get_list_timeline("startups", "pratikpoddar", "startups", 100)
#search_twitter("sachin tendulkar", 100)


