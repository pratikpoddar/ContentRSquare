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
import collections
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.collocations import *

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

    return ['No Results. Team working']

    time.sleep(20)
    woeid = location_woeid[location_name]

    try:
        trends = api.trends_place(woeid)[0]['trends']
    except Exception as e:
        trends = []

    trends = map(lambda x: x['name'], trends)
    return trends

def get_all_twitter_trends():
    output = {}
    for location in location_woeid.keys():
        output[location] = get_top_trends(location_name=location)
    return output

def get_twitter_stories(topic):
	twitter_text = ""
	all_words = []
	n=0
	stop = stopwords.words('english')
	keyword = 'Shah Rukh Khan'
	for tweet in tweepy.Cursor(api.search, q=keyword, rpp=200, result_type="recent", include_entities=True, geocode="", lang="en").items():
		n+=1
		if n==600:
			break
		text_string = tweet.text
		print text_string
		twitter_text += text_string.encode('utf8')
		twitter_text += '. '

	read_data = ""
	read_data = unicode(twitter_text, errors='ignore')

	n=0
	stop = stopwords.words('english')
	stop += ['rt', 'com', 'http', 'http://', '&amp;'] 
	replace_words = ['?', '(', ')', '"', '\n', ':', ',', '.', '#', 'http', '//t', '//']
	read_data = read_data.lower()
	for i in replace_words:
		read_data = read_data.replace(i, '')	

	tokens = read_data.split(' ')
	wnl = nltk.WordNetLemmatizer()
	wnl_tokens = [wnl.lemmatize(t) for t in tokens]
	words = [i for i in wnl_tokens if i not in stop]
	words = [i for i in words if len(i)>2]

	text = nltk.Text(words)
	most_common = nltk.FreqDist(text).most_common(50)

	tokens_bigram = re.split(r'\W+', read_data)
	wnl = nltk.WordNetLemmatizer()
	wnl_tokens = [wnl.lemmatize(t) for t in tokens_bigram]
	words = [i for i in wnl_tokens if i not in stop]
	words = [i for i in words if len(i)>2]

	bigram_measures = nltk.collocations.BigramAssocMeasures()
	word_fd = nltk.FreqDist(words)
	bigram_fd = nltk.FreqDist(nltk.bigrams(words))
	finder = BigramCollocationFinder(word_fd, bigram_fd)

	bigrams = finder.nbest(bigram_measures.raw_freq, 30)

	for word in most_common:
		print word

	print "-----"

	for bigram in bigrams:
		print bigram

	print "-----"

	all_bigrams = []
	for word in most_common:
		n=0
		word_bigrams=[]
		for bigram in bigrams:
			if word[0] in list(bigram):
				n+=1
				word_bigrams+=bigram
				all_bigrams+=bigram
		if n>1:
			# print a, m, "---", list(set(word_bigrams))
			print word[0], "---", list(set(word_bigrams))
			pass

	print "-----------"

	counter=collections.Counter(all_bigrams)
	for word in sorted(counter.items(), key=lambda x: x[1], reverse=True):
		print word

