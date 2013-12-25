import tweepy
import json
import jsonpickle
from time import sleep
import sys
import itertools
import urlutils

consumer_key="nNRGguiHtC5AouxzUlZQ"
consumer_secret="T3df1h6SIqitUs50mlPlbrTN9JrEMZzZK9h6ChYCGw"
access_token="66690578-TeOd1CQGR6KaF3cQvyNE59XPLYLJ7HAmu2DLLqTri"
access_token_secret="rGJYuYUJiSnUEqP0wxDNpfNVidPxZFqkuKkGDu3i3jI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

import gevent
from gevent import monkey
from gevent.pool import Pool

monkey.patch_all(thread=False)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def print_status(status):
	urls = map(lambda x: x['expanded_url'], status.entities['urls'])
	printable = ""
        if len(urls):
        	printable += "-----\n"
		urltitles = map(lambda x: urlutils.getUrlTitle(x), urls)
		for ut in urltitles:
			try:
				printable += str(ut['url'])+"\n"+str(removeNonAscii(ut['title']))+"\n"
			except:
				pass

	print printable
	return

def search_twitter(result_type, lang, loc, fromperson, filtertype):

	for tweet in tweepy.Cursor(api.search,
			q="filter:"+filtertype+" from:"+fromperson,
			rpp=100,
			result_type=result_type,
			include_entities=True,
			geocode=loc,
			lang=lang).items():
		print_status(tweet)

#search_twitter("recent", "en", "37.781157,-122.398720,10000mi", "pratikpoddar", "links")
#search_twitter("popular", "en", "", "pratikpoddar","news")

def get_list_timeline(owner, listname):

	status_list = [] # Create empty list to hold statuses
	cur_status_count = 0 # set current status count to zero

	try:
		statuses = api.list_timeline(count=200, owner_screen_name=owner, slug=listname, include_entities="1")
		while statuses != []:
		    cur_status_count = cur_status_count + len(statuses)
		    for status in statuses:
		        status_list.append(status)

		    # Get tweet id from last status in each page
		    theMaxId = statuses[-1].id
		    theMaxId = theMaxId - 1

		    statuses = api.list_timeline(count=200, owner_screen_name=owner, slug=listname, include_entities="1", max_id=theMaxId)
	except:
		pass

        pool = Pool(len(status_list))
        jobs = [pool.spawn(print_status , s) for s in status_list]
        pool.join()

#get_list_timeline("pratikpoddar", "startups")
if len(sys.argv)==3:
	get_list_timeline(sys.argv[1], sys.argv[2])


