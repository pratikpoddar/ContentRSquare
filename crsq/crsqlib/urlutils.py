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
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
		opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), ('Accept-Charset', 'utf-8')]
		url = url.encode('utf-8')
		resp = opener.open(url)
                if resp.getcode() == 200:
                        return resp.url.encode('utf-8')
                else:
	                logger.exception('urlutils - getLongUrl - ' + url + ' ' + str(resp.getcode()))
                        raise
        except Exception as e:
		logger.exception('urlutils - getLongUrl - ' + url + ' ' + str(e))
		raise

def isShortUrlPossibly(url):
	try:
		domain = url.replace("http","").replace(":","").replace("/","").replace("www.","").replace("www","").split(".")[0]
		if len(domain)<=5:
			return True
		if domain in ["tinyurl"]:
			return True

		try:
			tld=url.replace("http://","").replace("https://","").split("/")[0].split(".")[-1]
			if tld in ["es", "co", "ly", "me"]:
				return True
		except:
			tld=url.replace("http://","").replace("https://","").split(".")[-1]
			if tld in ["es", "co", "ly", "me"]:
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

	blocked_domains = ['instagram', 'imgur', 'pandora', 'facebook', 'twitter', 'i', 'ow', 'twitpic', 'paper', 'stackoverflow', 'github', 'm', 'youtube', 'vimeo', 'flickr', 'kindle', 'fb', 'vine', 'foursquare', 'myemail', 'picasa', 'picasaweb', 'webex', 'maps', 'f6s', 'xkcd', 'windowsphone', 'amazonaws', 'itunes', 'pixable', 'speedtest', 'on-msn', 'craigslist']

	if filter(lambda x: x in blocked_domains, urlparse(url)[1].split(".")):
		return False
	
	if not (urlparse(url)[2] + urlparse(url)[3] + urlparse(url)[4]).replace("/","").replace(" ",""):
		return False
	
	try:
		if urlparse(url)[2].split('.')[-1].lower() in ['jpg', 'png', 'gif', 'pdf', 'mp3', 'wav', 'mp4', 'jpeg']:
			return False
	except:
		pass

	return True
	

