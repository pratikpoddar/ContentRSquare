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
from geopy import geocoders 

logger = logging.getLogger(__name__)

consumer_key="nNRGguiHtC5AouxzUlZQ"
consumer_secret="T3df1h6SIqitUs50mlPlbrTN9JrEMZzZK9h6ChYCGw"
access_token="66690578-TeOd1CQGR6KaF3cQvyNE59XPLYLJ7HAmu2DLLqTri"
access_token_secret="rGJYuYUJiSnUEqP0wxDNpfNVidPxZFqkuKkGDu3i3jI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

locationmap_dict = {}

# Installed from https://code.google.com/p/geopy/wiki/GettingStarted
@lru_cache(maxsize=2048)
def locationmap(location):

	try:
		g = geocoders.GoogleV3()
		place, (lat, lng) = g.geocode(location)  
		return "GeoCoder " + place
	except:
		pass
 
	location = location.lower()
        if filter(lambda x: location.find(x)>-1, ["washington state", "seattle"]):
		return "Seattle"
	if filter(lambda x: location.find(x)>-1, ["stanford", "palo alto", "california", "los angeles", "san francisco", "silicon valley"]):
		return "SF"
	if location == "la":
		return "SF"
	if location.find('hong kong')>-1:
		return "HK"
        if filter(lambda x: location.find(x)>-1, ["nyc", "new york", "jersey", "atlanta", "baltimore", "maryland", "washington d.c.", "boston", "louisville"]):
		return "NY"
	if (location == "ny"):
		return "NY"
        if (location.endswith(', nj')==True) or (location.endswith(',nj')==True) or (location.endswith(', ny')==True)  or (location.endswith(',ny')==True):
                return "NY"
        if filter(lambda x: location.find(x)>-1, ["london", "uk", "united kingdom", "dublin", "ireland", "england"]):
		if location.find("new england")==-1:
			return "London"
	if (location.endswith(', ca')==True) or (location.endswith(',ca')==True):
		return "SF"
	if filter(lambda x: location.find(x)>-1, ["mumbai", "bombay"]):
		return "Mumbai"
        if filter(lambda x: location.find(x)>-1, ["bengaluru", "bangalore"]):
                return "Bangalore"
	if filter(lambda x: location.find(x)>-1, ["delhi"]):
		return "Delhi"
        if filter(lambda x: location.find(x)>-1, ["united states", "usa", "america", "north america", "white house"]):
		return "United States"
	
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
		members = map(lambda x: (x.screen_name, x.location, owner, slug), tlist.members())
		file = open(owner+"@"+slug+".pickle", 'w')
		pickle.dump(members, file)
		file.close()
		print owner + "@" + slug + ".pickle prepared"
		return members

twitter_lists = [ 
("https://twitter.com/milesj/lists/cfo","Business", None),
("https://twitter.com/milesj/lists/cmo","Business", None),
("https://twitter.com/verified/lists/business","Business", None),
("https://twitter.com/cnni/lists/business","Business", None),
("https://twitter.com/mashable/lists/celebrity","Entertainment", None),
("https://twitter.com/mashable/lists/music","Entertainment", None),
("https://twitter.com/verified/lists/entertainment","Entertainment", None),
("https://twitter.com/verified/lists/music","Entertainment", None),
("https://twitter.com/CNNPolitics/lists/cnn-political-team","Politics", None),
("https://twitter.com/cspan/lists/congressional-media","Politics", "Boston/NY/SF"),
("https://twitter.com/cspan/lists/foreign-leaders","Politics", None),
("https://twitter.com/cspan/lists/members-of-congress","Politics", "Boston/NY/SF"),
("https://twitter.com/cspan/lists/senators","Politics", "Boston/NY/SF"),
("https://twitter.com/cspan/lists/u-s-representatives","Politics", "Boston/NY/SF"),
("https://twitter.com/verified/lists/politics","Politics", None),
("https://twitter.com/verified/lists/world-leaders","Politics", None),
("https://twitter.com/verified/lists/us-congress","Politics", "Boston/NY/SF"),
("https://twitter.com/espn/lists/espn-boston","Sports", "Boston"),
("https://twitter.com/espn/lists/espn-los-angeles","Sports", "SF"),
("https://twitter.com/iDeskCNN/lists/cnn-world-sport","Sports", None),
("https://twitter.com/verified/lists/baseball","Sports", "Boston/NY/SF"),
("https://twitter.com/verified/lists/cricket","Sports", "Mumbai/Bangalore"),
("https://twitter.com/verified/lists/olympians","Sports", None),
("https://twitter.com/verified/lists/soccer","Sports", "Boston/NY/SF/London"),
("https://twitter.com/verified/lists/sports","Sports", None),
("https://twitter.com/verified/lists/nba","Sports", "Boston/NY/SF"),
("https://twitter.com/mashable/lists/tech","Technology", None),
("https://twitter.com/mashable/lists/startups-nyc-24","Technology", "NY"),
("https://twitter.com/mashable/lists/startups-silicon-valley-24","Technology", "SF"),
("https://twitter.com/Scobleizer/lists/most-influential-in-tech","Technology", None),
("https://twitter.com/Scobleizer/lists/tech-company-founders","Technology/Business", None),
("https://twitter.com/Scobleizer/lists/tech-news-brands","Technology", None),
("https://twitter.com/Scobleizer/lists/tech-news-people","Technology", None),
("https://twitter.com/verified/lists/technology","Technology", None),
("https://twitter.com/milesj/lists/cio","Technology/Business", None),
("https://twitter.com/Scobleizer/lists/tech-company-executives","Technology/Business", None),
("https://twitter.com/dkhare/lists/india-tech-and-vc","Technology/Business", None),
("https://twitter.com/tellychakkar/lists/celebs","Entertainment", "Mumbai"),
("https://twitter.com/WSJ/lists/wsj-ceo-council","Business", None),
("https://twitter.com/WSJ/lists/wsj-tech","Technology", None),
("https://twitter.com/WSJ/lists/wsj-money","Business", None),
("https://twitter.com/WSJ/lists/wsj-sports","Sports", None),
("https://twitter.com/WSJ/lists/wsj-style-entertainment","Entertainment", None),
("https://twitter.com/WSJ/lists/wsj-politics","Politics", None),
("https://twitter.com/WSJ/lists/entertainment","Entertainment", None),
("https://twitter.com/WSJ/lists/business","Business", None),
("https://twitter.com/WSJ/lists/sports-news","Sports", None),
("https://twitter.com/TheWeek/lists/politics","Politics", None),
("https://twitter.com/TheWeek/lists/sports-news","Sports", None),
("https://twitter.com/TheWeek/lists/tech-news","Technology", None),
("https://twitter.com/TheWeek/lists/business-news","Business", None),
]

list_of_influencers = []
for tl in twitter_lists:
	list_of_influencers += get_members_of_list(tl[0])

screen_names = list(set(map(lambda x: x[0], list_of_influencers)))
twitter_location_dict = {}
twitter_location_renamed_dict = {}
ownerslug_dict = {}
proposed_sectors_dict = {}
proposed_location_dict = {}


for screen_name in screen_names:
	twitter_location_dict[screen_name] = []
	twitter_location_renamed_dict[screen_name] = []
	ownerslug_dict[screen_name] = []
	proposed_sectors_dict[screen_name] = []
	proposed_location_dict[screen_name] = []

for influencer in list_of_influencers:
	twitter_location_dict[influencer[0]] += [influencer[1]]
	twitter_location_renamed_dict[influencer[0]] += [locationmap(influencer[1])]
	print str(twitter_location_dict[influencer[0]]) + " --> " + str(twitter_location_renamed_dict[influencer[0]])
	ownerslug_dict[influencer[0]] += [(influencer[2], influencer[3])]
	proposed_sectors_dict[influencer[0]] += [filter(lambda x: x[0]=="https://twitter.com/"+ influencer[2] + "/lists/" + influencer[3], twitter_lists)[0][1]]
	proposed_location_dict[influencer[0]] += [filter(lambda x: x[0]=="https://twitter.com/"+ influencer[2] + "/lists/" + influencer[3], twitter_lists)[0][2]]


for screen_name in screen_names[:200]:
	print "---"
	print screen_name
	print list(set(ownerslug_dict[screen_name]))
	print list(set(twitter_location_dict[screen_name]))
	print list(set(twitter_location_renamed_dict[screen_name]))
	print list(set(proposed_sectors_dict[screen_name]))
	print list(set(proposed_location_dict[screen_name]))


