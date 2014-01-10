import tweepy
import json
import jsonpickle
from time import sleep
import sys
import itertools
from crsqlib import urlutils
import gevent
from gevent import monkey
from gevent.pool import Pool
import hashlib
import pickledb

consumer_key="nNRGguiHtC5AouxzUlZQ"
consumer_secret="T3df1h6SIqitUs50mlPlbrTN9JrEMZzZK9h6ChYCGw"
access_token="66690578-TeOd1CQGR6KaF3cQvyNE59XPLYLJ7HAmu2DLLqTri"
access_token_secret="rGJYuYUJiSnUEqP0wxDNpfNVidPxZFqkuKkGDu3i3jI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

monkey.patch_all(thread=False)

sinceiddb = pickledb.load('sinceidsaveddata.db', False)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def is_url_an_article(url):
        return url.replace("https:","").replace("http:","").replace("/","").replace("www.","").replace("www","").split(".")[0] not in ['instagram', 'imgur', 'pandora', 'facebook', 'i', 'ow', 'twitpic']

def print_status(status):
	urls = map(lambda x: x['expanded_url'], status.entities['urls'])
	printable = ""
        urltitles = filter(lambda x: is_url_an_article(x['url']), filter(lambda x: x, map(lambda x: urlutils.getCanonicalUrlTitle(x), urls)))
	
	if len(urltitles):
		printable += "-----\n"
		for ut in urltitles:
			try:
				printable += str(ut['url'])+"\n"+str(removeNonAscii(ut['title']))+"\n"
			except:
				pass

			try:
				printable += str(urlutils.getSocialShares(ut['url']))+"\n"
			except:
				pass

		print printable

	return

def search_twitter(result_type, lang, loc, fromperson, filtertype, keyword, numlinks):

	status_list = []

	hashval = str(int(hashlib.md5(str(result_type)+str(lang)+str(loc)+str(fromperson)+str(filtertype)+str(keyword)+str(numlinks)).hexdigest(), 16))
	if sinceiddb.get(hashval)==None:
		theSinceId = None
	else:
		theSinceId = int(sinceiddb.get(hashval))

	for tweet in tweepy.Cursor(api.search,
			q=keyword+" filter:"+filtertype+" from:"+fromperson,
			rpp=100,
			result_type=result_type,
			include_entities=True,
			geocode=loc,
			lang=lang).items():
		status_list.append(tweet)
		if len(status_list)>numlinks:
			break
		if tweet.id < theSinceId:
			break

	if status_list:
	        pool = Pool(len(status_list))
	        jobs = [pool.spawn(print_status , s) for s in status_list]
	        pool.join(timeout=30)
	
		try:
	        	sinceiddb.set(hashval, status_list[0].id)
	        	sinceiddb.dump()
		except:
			pass

	return

def get_list_timeline(owner, listname, numlinks):

	status_list = [] # Create empty list to hold statuses

        hashval = str(int(hashlib.md5(str(owner)+str(listname)+str(numlinks)).hexdigest(), 16))
        if sinceiddb.get(hashval)==None:
                theSinceId = None
        else:
                theSinceId = int(sinceiddb.get(hashval))

	try:
		statuses = api.list_timeline(count=50, owner_screen_name=owner, slug=listname, include_entities="1", since_id=theSinceId)
		while (statuses != []) and (len(status_list)<numlinks):
		    for status in statuses:
			status_list.append(status)
		    
		    # Get tweet id from last status in each page
		    theMaxId = statuses[-1].id
		    theMaxId = theMaxId - 1

		    statuses = api.list_timeline(count=50, owner_screen_name=owner, slug=listname, include_entities="1", max_id=theMaxId, since_id=theSinceId)
	except Exception as e:
		print e
		pass

	if status_list:
	        pool = Pool(len(status_list))
	        jobs = [pool.spawn(print_status , s) for s in status_list]
	        pool.join(timeout=30)

	        try:
			sinceiddb.set(hashval, status_list[0].id)
			sinceiddb.dump()	
		except:
			pass
	
	return

#get_list_timeline("pratikpoddar", "startups", 100)
if len(sys.argv)==3:
	get_list_timeline(sys.argv[1], sys.argv[2], 100)

#search_twitter("recent", "en", "37.781157,-122.398720,10000mi", "pratikpoddar", "links","", 100)
#search_twitter("popular", "en", "", "pratikpoddar","news","", 100)
if len(sys.argv)==2:
	search_twitter("recent", "en", "", "", "news", sys.argv[1], 100)


