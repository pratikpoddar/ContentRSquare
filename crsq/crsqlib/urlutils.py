import urllib2
from bs4 import BeautifulSoup
from urlnorm import norm
from urlparse import parse_qs, urlsplit, urlunsplit
from urllib import urlencode
from cgi import escape
import simplejson
from functools32 import lru_cache

@lru_cache(maxsize=512)
def getCanonicalUrl(url):
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
    return norm(urlunsplit(res))

@lru_cache(maxsize=1024)
def getSocialShares(url):
	
	fb = 0
	tw = 0
	try:
		fb = simplejson.load(urllib2.urlopen("http://graph.facebook.com/?ids=" + url))[url]['shares']
	except:
		pass
	
	try:
		tw = simplejson.load(urllib2.urlopen("http://urls.api.twitter.com/1/urls/count.json?url="+url))['count']
	except:
		pass

	return {'fb': fb, 'tw': tw}

def getLongUrl(url):
        try:
                resp = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
                if resp.getcode() == 200:
                        return resp.url
                else:
                        return None
        except Exception as e:
		print str(e)
		raise

def isShortUrlPossibly(url):
	domain = url.replace("http","").replace(":","").replace("/","").replace("www.","").replace("www","").split(".")[0]
	if len(domain)<=5:
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

def getLongUrlOptimized(url):
	if isShortUrlPossibly(url):
		longurl = getLongUrl(url)
		return longurl
	else:
		return url


def is_url_an_article(url):
        return url.replace("https:","").replace("http:","").replace("/","").replace("www.","").replace("www","").split(".")[0] not in ['instagram', 'imgur', 'pandora', 'facebook', 'i', 'ow', 'twitpic']

