import urllib2
from bs4 import BeautifulSoup
from urlnorm import norm
from urlparse import parse_qs, urlsplit, urlunsplit
from urllib import urlencode
from cgi import escape
import simplejson
from functools32 import lru_cache
import logging
from urlparse import urlparse
from cookielib import CookieJar
import re
import requests
from crsq.crsqlib.stringutils import *

logger = logging.getLogger(__name__)

@lru_cache(maxsize=512)
def getCanonicalUrl(url):
    try:
	    if not url:
		return None
	
	    url = crsq_unicode(url)
	    res = urlsplit(url)

	    # if google news article
	    if res.query:
		    qdict = parse_qs(res.query)
		    if (res[1] == 'news.google.com') and (res[2] == '/news/url') and ('url' in qdict.keys()):
			return getCanonicalUrl(qdict['url'][0])
	
	    if res.query:
		    qdict = parse_qs(res.query)
		    map(lambda key: qdict.pop(key), filter(lambda key: key.startswith('utm_'), qdict.keys()))
		    map(lambda key: qdict.pop(key), filter(lambda key: re.match('^tu[0-9]+$',key), qdict.keys()))
		    qtuple = map(lambda t: (t[0], t[1][0]), qdict.items())
		    qtuple.sort(key=lambda x: x[0])
		    res = list(res)
		    res[3] = urlencode(qtuple, doseq=1)
	    else:
		    res = list(res)
	    res[4] = ''
	    return crsq_unicode(norm(urlunsplit(res)))
    except Exception as e:
	    logger.exception('urlutils - getCanonicalUrl - ' + url + ' ' + str(e))
	    raise

@lru_cache(maxsize=1024)
def getSocialShares(url):

	url = crsq_unicode(url)
	fb = 0
	tw = 0
	try:
		fb = int(simplejson.load(urllib2.urlopen("http://graph.facebook.com/?ids=" + url, timeout=3))[url]['shares'])
	except Exception as e:
		pass
	
	try:
		tw = int(simplejson.load(urllib2.urlopen("http://urls.api.twitter.com/1/urls/count.json?url="+url, timeout=3))['count'])
	except Exception as e:
		pass

	return {'fb': fb, 'tw': tw}

def getLongUrl(url):
        try:
		url = crsq_unicode(url)
		r = requests.get(url, timeout=8)
		return getCanonicalUrl(crsq_unicode(r.url))
		#cj = CookieJar()
		#cj.clear()
                #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		#try:
		#	resp = opener.open(url, timeout=5)
	        #       if resp.getcode() == 200:
        	#               return crsq_unicode(resp.url)
		#except urllib2.HTTPError as err:
		#	if err.code == 403:
		#		opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11 Chrome/32.0.1700.77 Safari/537.36'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'), ('Accept-Encoding','gzip,deflate,sdch'), ('Connection', 'keep-alive')]
		#		resp = opener.open(url, timeout=5)
		#		if resp.getcode() == 200:
		#			return crsq_unicode(resp.url)
		#	else:
		#		raise
		#except Exception as e:
		#	logger.exception('urlutils - getLongUrl - ' + url + ' ' + str(e))
		#	raise
		
		#logger.exception('urlutils - getLongUrl - ' + url)
		#raise

        except Exception as e:
		logger.exception('urlutils - getLongUrl - ' + url + ' ' + str(e))
		raise

def isShortUrlPossibly(url):
	try:
		url = getCanonicalUrl(crsq_unicode(url))
		domain = urlparse(url)[1].replace('www.','')
		if len(domain)<=8:
			return True
		if "tinyurl" in domain.split("."):
			return True
		if "feedly" in domain.split("."):
			return True
		if "bitly" in domain.split("."):
			return True
		if "mklnd" in domain.split("."):
			return True
                if "amzn" in domain.split("."):
                        return True
		if len(filter(lambda x: len(filter(lambda y: y in x, ["a", "e", "i", "o", "u"]))==0, domain.replace('www.', '').split(".")[:-1]))>0:
			return True
		
		topdomain = '.'.join(urlparse(url)[1].split(".")[-2:])
		if len(topdomain)<=7:
			return True

		tld=urlparse(url)[1].split(".")[-1]
		if tld in ["es", "co", "ly", "me", "it", "bg", "to", "ac", "io", "st", "gs", "mu", "tc", "tw", "ai", "sh", "nl", "at", "in", "asia", "de", "tl", "cc", "us", "ie", "ms", "ws", "ch", "mn", "ps", "ne", "be", "vu", "ve", "se", "er", "re", "ro","or"]:
			return True
	
		subdomain=urlparse(url)[1].split(".")[0]
		if subdomain in ["on"]:
			return True
		
		return False
	except Exception as e:
                logger.exception('urlutils - isShortUrlPossibly - ' + url + ' ' + str(e))
		raise

def getLongUrlOptimized(url):
	try:
		if isShortUrlPossibly(url):
			longurl = getLongUrl(url)
			return getCanonicalUrl(longurl)
		else:
			return getCanonicalUrl(url)
	except:
		raise


def is_url_an_article(url):
	
	url = crsq_unicode(url)

	blocked_domains = ['instagram', 'imgur', 'pandora', 'facebook', 'twitter', 'i', 'ow', 'twitpic', 'paper', 'stackoverflow', 'github', 'm', 'youtube', 'vimeo', 'flickr', 'kindle', 'fb', 'vine', 'foursquare', 'myemail', 'picasa', 'picasaweb', 'webex', 'maps', 'f6s', 'xkcd', 'windowsphone', 'amazonaws', 'itunes', 'pixable', 'speedtest', 'on-msn', 'craigslist', 'stocktwits', 'rt', 'sharedby', 'kickstarter', 'arxiv', 'stks', 'webcast', 'mobile', 'live', 'pinterest', 'map', 'reddit', 'youtu', 'twishort', 'dailymotion', 'tumblr', 'plus', 'store', 'apple', 'tmblr', 'video', 'smarturl', 'feedburner', 'spoti', 'spotify', 'ycombinator', 'wikipedia', 'tv', 'email', 'jobvite', 'theresumator', 'twittercounter', 'sumall', 'flipboard', 'shareable', 'chumly', 'cartrade', 'path', 'visual', 'amazon', '4shared', 'viralglobalnews', 'producthunt']

	if filter(lambda x: x in blocked_domains, urlparse(url)[1].split(".")):
		return False

        if "google" in urlparse(url)[1].split("."):
                if url.find("www.google.com/hostednews")==-1:
                        return False

	if not (urlparse(url)[2] + urlparse(url)[3] + urlparse(url)[4]).replace("/","").replace(" ",""):
		return False
	
	try:
		if urlparse(url)[2].split('.')[-1].lower() in ['jpg', 'png', 'gif', 'pdf', 'mp3', 'wav', 'mp4', 'jpeg', 'xml', 'zip', 'gzip', 'tar']:
			return False
	except:
		pass

	if (url.find("/signup")>-1) or (url.find("/login")>-1):
		return False

	if len(url)>250:
		return False
	
	return True
	

