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

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def print_status(status):
	urls = map(lambda x: x['expanded_url'], status.entities['urls'])
        if len(urls):
        	print "-----"
                print map(lambda x: urlutils.getLongUrlOptimized(x), urls)
                #print status.text
                breakpoints = map(lambda x: x['indices'], status.entities['urls']+status.entities['user_mentions'])
                breakpoints = sorted(sum(breakpoints + [[0, len(status.text)]], []))
                printable_status = ""
                for i in range(0,len(breakpoints)/2):
                        printable_status += status.text[breakpoints[2*i]:breakpoints[2*i+1]]
		printable_status = printable_status.replace('RT ', '').replace(':','').replace('\n',' ').replace('  ',' ').replace('  ',' ').strip()
                print removeNonAscii(printable_status)
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
	statuses = api.list_timeline(count=200, owner_screen_name=owner, slug=listname, include_entities="1")
	while statuses != []:
	    cur_status_count = cur_status_count + len(statuses)
	    for status in statuses:
	        status_list.append(status)

	    # Get tweet id from last status in each page
	    theMaxId = statuses[-1].id
	    theMaxId = theMaxId - 1

	    statuses = api.list_timeline(count=200, owner_screen_name=owner, slug=listname, include_entities="1", max_id=theMaxId)

	for status in status_list:
		print_status(status)

get_list_timeline("pratikpoddar", "startups")

