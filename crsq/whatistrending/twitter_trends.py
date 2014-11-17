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
    'India' : 23424848,
    'Bangalore' : 2295420,
    'Mumbai' : 2295411,
    'New York' : 2459115,
    'London' : 44418,
}

@lru_cache(maxsize=1024)
def trends(location_name='India'):
    ## woeid for india is 23424848

    woeid = location_woeid[location_name]

    try:
        trends = api.trends_place(woeid)[0]['trends']
    except Exception as e:
        trends = []

    trends = map(lambda x: x['name'], trends)
    return trends


