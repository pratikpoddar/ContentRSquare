import tweepy
import json
import jsonpickle
from time import sleep
import sys
import itertools
import hashlib
import logging
from urlparse import urlparse
from functools32 import lru_cache
import pickle
from django.template.defaultfilters import slugify
from geopy import geocoders, distance

logger = logging.getLogger(__name__)

consumer_key="eULM1PaB0Aw7RQyvWbRzHA"
consumer_secret="d9h1QnZE7PAh7DVmQO8yapgRptVoIu8yTlzisytR2YQ"
access_token="66690578-Upv2U0brunkUKvP0W1IVHnS2z3wVeFS2EBSEV5J9z"
access_token_secret="h2JlCEUGVLkD1ZYJJiDkXXFQ4Gw19EpVk2E2Y8EEeq2OI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

g = geocoders.GoogleV3()

locationmap_dict = {}

centralcities = {"mumbai-india": g.geocode("Mumbai, India"), "bangalore-india": g.geocode("Bangalore, India"), "san-francisco-usa": g.geocode("San Francisco, California"), "boston-usa": g.geocode("Boston, MA, United States"), "london-uk": g.geocode("London, UK"), "new-york-usa": g.geocode("New York, USA")}

# Installed from https://code.google.com/p/geopy/wiki/GettingStarted
@lru_cache(maxsize=2048)
def locationmap(location):

	try:
		place, (lat, lng) = g.geocode(location)  
		distcc = map(lambda cc: (cc[0], distance.distance((lat, lng), cc[1][1]).miles), centralcities.items())
		distcc.sort(key=lambda x: x[1])
		return slugify(distcc[0][0])
	except Exception as e:
		return None

def locationmap_strmatch(location): 
	location = location.lower()
        if filter(lambda x: location.find(x)>-1, ["massachusets", "boston"]):
		return ["boston-usa"]
	if filter(lambda x: location.find(x)>-1, ["stanford", "palo alto", "california", "los angeles", "san francisco", "silicon valley"]):
		return ["san-francisco-usa"]
	if location == "la":
		return ["san-francisco-usa"]
	if location.find('hong kong')>-1:
		return ["bangalore-india"]
        if filter(lambda x: location.find(x)>-1, ["nyc", "new york", "jersey", "atlanta", "baltimore", "maryland", "washington d.c.", "boston", "louisville"]):
		return ["new-york-usa"]
	if (location == "ny"):
		return ["new-york-usa"]
        if (location.endswith(', nj')==True) or (location.endswith(',nj')==True) or (location.endswith(', ny')==True)  or (location.endswith(',ny')==True):
                return ["new-york-usa"]
        if filter(lambda x: location.find(x)>-1, ["london", "uk", "united kingdom", "dublin", "ireland", "england"]):
		if location.find("new england")==-1:
			return ["london-uk"]
	if (location.endswith(', ca')==True) or (location.endswith(',ca')==True):
		return ["san-francisco-usa"]
	if filter(lambda x: location.find(x)>-1, ["mumbai", "bombay", "delhi"]):
		return ["mumbai-india"]
        if filter(lambda x: location.find(x)>-1, ["bengaluru", "bangalore"]):
                return ["bangalore-india"]
        if filter(lambda x: location.find(x)>-1, ["united states", "usa", "america", "north america", "white house"]):
		return ["boston-usa", "san-francisco-usa", "new-york-usa"]
	
	return None

def get_members_of_list(linkoflist):
	ownerslug = urlparse(linkoflist)[2].split("/lists/")
	owner = ownerslug[0].replace("/","")
	slug = ownerslug[1].replace("/","")
	print owner + " @ " + slug
	
	try:
		file = open(owner+"@"+slug+".pickle", 'r')
		return pickle.load(file)
	except:
		tlist = api.get_list(owner_screen_name=owner, slug=slug)
		members = map(lambda x: (x.screen_name, x.location, owner, slug, x.id), tlist.members())
		file = open(owner+"@"+slug+".pickle", 'w')
		pickle.dump(members, file)
		file.close()
		print owner + "@" + slug + ".pickle prepared"
		return members

twitter_lists = [ 
("https://twitter.com/milesj/lists/cfo",["business"], []),
("https://twitter.com/milesj/lists/cmo",["business"], []),
("https://twitter.com/verified/lists/business",["business"], []),
("https://twitter.com/cnni/lists/business",["business"], []),
("https://twitter.com/mashable/lists/celebrity",["entertainment"], []),
("https://twitter.com/mashable/lists/music",["entertainment"], []),
("https://twitter.com/verified/lists/entertainment",["entertainment"], []),
("https://twitter.com/verified/lists/music",["entertainment"], []),
("https://twitter.com/CNNPolitics/lists/cnn-political-team",["politics"], []),
("https://twitter.com/cspan/lists/congressional-media",["politics"], ["boston-usa", "san-francisco-usa", "new-york-usa"]),
("https://twitter.com/cspan/lists/foreign-leaders",["politics"], []),
("https://twitter.com/cspan/lists/members-of-congress",["politics"], ["boston-usa", "san-francisco-usa", "new-york-usa"]),
("https://twitter.com/cspan/lists/senators",["politics"], ["boston-usa", "san-francisco-usa", "new-york-usa"]),
("https://twitter.com/cspan/lists/u-s-representatives",["politics"], ["boston-usa", "san-francisco-usa", "new-york-usa"]),
("https://twitter.com/verified/lists/politics",["politics"], []),
("https://twitter.com/verified/lists/world-leaders",["politics"], []),
("https://twitter.com/verified/lists/us-congress",["politics"], ["boston-usa", "san-francisco-usa", "new-york-usa"]),
("https://twitter.com/espn/lists/espn-boston",["sports"], ["boston-usa"]),
("https://twitter.com/espn/lists/espn-los-angeles", ["sports"], ["san-francisco-usa"]),
("https://twitter.com/iDeskCNN/lists/cnn-world-sport",["sports"], []),
("https://twitter.com/verified/lists/baseball",["sports"], ["boston-usa", "san-francisco-usa", "new-york-usa"]),
("https://twitter.com/verified/lists/cricket",["sports"], ["mumbai-india", "bangalore-india"]),
("https://twitter.com/verified/lists/olympians",["sports"], []),
("https://twitter.com/verified/lists/soccer",["sports"], ["boston-usa", "san-francisco-usa", "new-york-usa", "london-uk"]),
("https://twitter.com/verified/lists/sports",["sports"], []),
("https://twitter.com/verified/lists/nba",["sports"], ["boston-usa", "san-francisco-usa", "new-york-usa"]),
("https://twitter.com/mashable/lists/tech",["technology"], []),
("https://twitter.com/mashable/lists/startups-nyc-24",["technology"], ["new-york-usa"]),
("https://twitter.com/mashable/lists/startups-silicon-valley-24",["technology"], ["san-francisco-usa"]),
("https://twitter.com/Scobleizer/lists/most-influential-in-tech",["technology"], []),
("https://twitter.com/Scobleizer/lists/tech-company-founders", ["technology", "business"], []),
("https://twitter.com/Scobleizer/lists/tech-news-brands", ["technology"], []),
("https://twitter.com/Scobleizer/lists/tech-news-people", ["technology"], []),
("https://twitter.com/verified/lists/technology", ["technology"], []),
("https://twitter.com/milesj/lists/cio", ["technology", "business"], []),
("https://twitter.com/Scobleizer/lists/tech-company-executives",["technology", "business"], []),
("https://twitter.com/dkhare/lists/india-tech-and-vc", ["technology", "business"], []),
("https://twitter.com/tellychakkar/lists/celebs",["entertainment"], ["bangalore-india", "mumbai-india"]),
("https://twitter.com/WSJ/lists/wsj-ceo-council",["business"], []),
("https://twitter.com/WSJ/lists/wsj-tech",["technology"], []),
("https://twitter.com/WSJ/lists/wsj-money",["business"], []),
("https://twitter.com/WSJ/lists/wsj-sports",["sports"], []),
("https://twitter.com/WSJ/lists/wsj-style-entertainment",["entertainment"], []),
("https://twitter.com/WSJ/lists/wsj-politics",["politics"], []),
("https://twitter.com/WSJ/lists/entertainment",["entertainment"], []),
("https://twitter.com/WSJ/lists/business",["business"], []),
("https://twitter.com/WSJ/lists/sports-news",["sports"], []),
("https://twitter.com/TheWeek/lists/politics",["politics"], []),
("https://twitter.com/TheWeek/lists/sports-news",["sports"], []),
("https://twitter.com/TheWeek/lists/tech-news",["technology"], []),
("https://twitter.com/TheWeek/lists/business-news",["business"], []),
]

list_of_influencers = []
for tl in twitter_lists:
	list_of_influencers += get_members_of_list(tl[0])

screen_names = list(set(map(lambda x: x[0], list_of_influencers)))
print(len(screen_names))
id_dict = {}
twitter_location_dict = {}
twitter_location_renamed_dict = {}
twitter_location_strmatch_dict = {}
ownerslug_dict = {}
proposed_sectors_dict = {}
proposed_location_dict = {}


for screen_name in screen_names:
	id_dict[screen_name] = []
	twitter_location_dict[screen_name] = []
	twitter_location_renamed_dict[screen_name] = []
	twitter_location_strmatch_dict[screen_name] = []
	ownerslug_dict[screen_name] = []
	proposed_sectors_dict[screen_name] = []
	proposed_location_dict[screen_name] = []

list_of_influencers = []
for influencer in list_of_influencers:
	id_dict[influencer[0]] += [influencer[4]]
	twitter_location_dict[influencer[0]] += [influencer[1]]
	twitter_location_renamed_dict[influencer[0]] += locationmap(influencer[1])
	twitter_location_strmatch_dict[influencer[0]] += locationmap_strmatch(influencer[1])
	ownerslug_dict[influencer[0]] += [(influencer[2], influencer[3])]
	proposed_sectors_dict[influencer[0]] += map(lambda x: slugify(x), filter(lambda x: x[0]=="https://twitter.com/"+ influencer[2] + "/lists/" + influencer[3], twitter_lists)[0][1])
	print filter(lambda x: x[0]=="https://twitter.com/"+ influencer[2] + "/lists/" + influencer[3], twitter_lists)[0][2]
	proposed_location_dict[influencer[0]] += map(lambda x: slugify(x), filter(lambda x: x[0]=="https://twitter.com/"+ influencer[2] + "/lists/" + influencer[3], twitter_lists)[0][2])


final_output = []
for screen_name in screen_names:
	print "---"
	print screen_name
	#api.add_list_member(owner_screen_name="pratikpoddar", slug='crsq-influencers-1', user_id=int(id_dict[screen_name][0]))
	print list(set(ownerslug_dict[screen_name]))
	print list(set(twitter_location_dict[screen_name]))
	print list(set(twitter_location_renamed_dict[screen_name]))
        print list(set(proposed_location_dict[screen_name]))
        print list(set(twitter_location_strmatch_dict[screen_name]))
	print list(set(proposed_sectors_dict[screen_name]))
	final_output.append((screen_name, list(set(twitter_location_renamed_dict[screen_name])), list(set(proposed_location_dict[screen_name])), list(set(twitter_location_strmatch_dict[screen_name])), list(set(proposed_sectors_dict[screen_name]))))

file = open("final_output.pickle", 'w')
pickle.dump(final_output, file)
file.close()

