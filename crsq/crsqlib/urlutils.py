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

logger = logging.getLogger(__name__)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

@lru_cache(maxsize=512)
def getCanonicalUrl(url):
    try:
	    if not url:
		return None
	
	    res = urlsplit(url)
	    if res.query:
		    qdict = parse_qs(res.query)
		    map(lambda key: qdict.pop(key), filter(lambda key: key.startswith('utm_'), qdict.keys()))
		    res = list(res)
		    res[3] = escape(urlencode(qdict, doseq=1))
	    else:
		    res = list(res)
	    res[4] = ''
	    return norm(urlunsplit(res)).encode('utf-8')
    except Exception as e:
	    logger.exception('urlutils - getCanonicalUrl - ' + url + ' ' + str(e))
	    raise

@lru_cache(maxsize=1024)
def getSocialShares(url):
	
	fb = 0
	tw = 0
	try:
		fb = simplejson.load(urllib2.urlopen("http://graph.facebook.com/?ids=" + url))[url]['shares']
	except Exception as e:
		logger.debug('urlutils - getSocialShares - ' + url + ' ' + str(e))
	
	try:
		tw = simplejson.load(urllib2.urlopen("http://urls.api.twitter.com/1/urls/count.json?url="+url))['count']
	except Exception as e:
		logger.debug('urlutils - getSocialShares - ' + url + ' ' + str(e))

	return {'fb': fb, 'tw': tw}

def getLongUrl(url):
        try:
		cj = CookieJar()
		cj.clear()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		url = url.encode('utf-8')
		try:
			resp = opener.open(url, timeout=5)
	                if resp.getcode() == 200:
        	                return resp.url.encode('utf-8')
		except urllib2.HTTPError as err:
			if err.code == 403:
				opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11 Chrome/32.0.1700.77 Safari/537.36'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'), ('Accept-Encoding','gzip,deflate,sdch'), ('Connection', 'keep-alive')]
				resp = opener.open(url, timeout=5)
				if resp.getcode() == 200:
					return resp.url.encode('utf-8')
			else:
				raise
		except Exception as e:
			logger.exception('urlutils - getLongUrl - ' + url + ' ' + str(e))
			raise
		
		logger.exception('urlutils - getLongUrl - ' + url)
		raise

        except Exception as e:
		logger.exception('urlutils - getLongUrl - ' + url + ' ' + str(e))
		raise

def isShortUrlPossibly(url):
	try:
		domain = urlparse(url)[1].replace('www.','')
		if len(domain)<=7:
			return True
		if "tinyurl" in domain.split("."):
			return True

		topdomain = '.'.join(urlparse(url)[1].split(".")[-2:])
		if len(topdomain)<=7:
			return True

		tld=urlparse(url)[1].split(".")[-1]
		if tld in ["es", "co", "ly", "me", "it", "bg", "to", "ac", "io", "st", "gs", "mu", "tc", "tw", "ai"]:
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
			return longurl
		else:
			return url
	except:
		raise


def is_url_an_article(url):

	blocked_domains = ['instagram', 'imgur', 'pandora', 'facebook', 'twitter', 'i', 'ow', 'twitpic', 'paper', 'stackoverflow', 'github', 'm', 'youtube', 'vimeo', 'flickr', 'kindle', 'fb', 'vine', 'foursquare', 'myemail', 'picasa', 'picasaweb', 'webex', 'maps', 'f6s', 'xkcd', 'windowsphone', 'amazonaws', 'itunes', 'pixable', 'speedtest', 'on-msn', 'craigslist', 'stocktwits', 'rt', 'sharedby', 'kickstarter', 'arxiv', 'stks', 'webcast', 'mobile', 'live', 'pinterest', 'map', 'reddit', 'youtu', 'twishort', 'dailymotion', 'tumblr', 'plus', 'store', 'apple', 'tmblr', 'video', 'smarturl', 'feedburner', 'spoti', 'spotify']

	if filter(lambda x: x in blocked_domains, urlparse(url)[1].split(".")):
		return False
	
	if not (urlparse(url)[2] + urlparse(url)[3] + urlparse(url)[4]).replace("/","").replace(" ",""):
		return False
	
	try:
		if urlparse(url)[2].split('.')[-1].lower() in ['jpg', 'png', 'gif', 'pdf', 'mp3', 'wav', 'mp4', 'jpeg', 'xml']:
			return False
	except:
		pass

	return True
	

