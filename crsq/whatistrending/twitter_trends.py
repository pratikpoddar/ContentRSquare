import tweepy
from tweepy import Cursor
from functools32 import lru_cache
import goose
import requests
from bs4 import BeautifulSoup
import simplejson
import re
import time
from cookielib import CookieJar
import logging
from crsq.crsqlib.stringutils import *

consumer_key="1up7tIphvvw9AAkBnvbHTNMjc"
consumer_secret="dvUGo4u0e3Iw9GieBzneE0mHy5noqi4t8rdQKXgogGPsFH8dcB"
access_token="2775880520-Qc5d9AqfKLvBZTODE7k2pv6y8zzJN5JYfSDALjO"
access_token_secret="SUBilPqKRGeqJYRWMxCjyt26pIp7MmtTmk6mlSTmdDk8P"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


location_woeid = {
'United Kingdom':23424975,
'Bangalore':2295420,
'South Africa':23424942,
'Netherlands':23424909,
'Canada':23424775,
'Worldwide':1,
'United States':23424977,
'Washington':2514815,
'Chennai':2295424,
'Indonesia':23424846,
'Delhi':20070458,
'Paris':615702,
'Tokyo':1118370,
'Singapore':23424948,
'India':23424848,
'Australia':23424748,
'Spain':23424950,
'France':23424819,
'Italy':23424853,
'San Francisco':2487956,
'New York':2459115,
'Japan':23424856,
'Germany':23424829,
'Mumbai':2295411,
'Malaysia':23424901,
'Russia':23424936,
'London':44418,
}

@lru_cache(maxsize=1024)
def get_top_trends(location_name='India'):
    ## woeid for india is 23424848

    time.sleep(20)
    woeid = location_woeid[location_name]

    try:
        trends = api.trends_place(woeid)[0]['trends']
    except Exception as e
        trends = []

    trends = map(lambda x: x['name'], trends)
    return trends

@lru_cache(maxsize=1024)
def get_all_twitter_trends():
    output = {}
    for location in location_woeid.keys():
        output[location] = get_top_trends(location_name=location)
    return output


        

