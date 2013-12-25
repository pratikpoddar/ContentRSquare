import urllib2
from bs4 import BeautifulSoup
from urlnorm import norm
from urlparse import parse_qs, urlsplit, urlunsplit
from urllib import urlencode
from cgi import escape

def getCanonicalUrl(url):
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

def getCanonicalUrlTitle(url):
	try:
		#resp = urllib2.urlopen(url)
		resp = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
		if resp.getcode() == 200:
			try:
				return {'url': getCanonicalUrl(resp.geturl()), 'title': BeautifulSoup(resp).title.string.replace('\t','').replace('\n','').strip()}
			except Exception as e:
				raise
		else:
			raise
	except Exception as e:
		return None

def getLongUrl(tinyurl):
        try:
                resp = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
                #resp = urllib2.urlopen(tinyurl)
                if resp.getcode() == 200:
                        return resp.url
                else:
                        return None
        except:
                return None

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


