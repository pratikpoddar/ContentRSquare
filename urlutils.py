import urllib
import redis

redis_data = redis.Redis("localhost")

def getLongUrl(tinyurl):
	try:
		resp = urllib.urlopen(tinyurl)
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
		tld=url.replace("http://","").replace("https://","").split("/")[-1].split(".")[-1]
		if tld in ["es", "co", "ly"]:
			return True
	except:
		tld=url.replace("http://","").replace("https://","").split(".")[-1]
		if tld in ["es", "co", "ly", "me"]:
			return True
	return False

def getLongUrlOptimized(url):
	if isShortUrlPossibly(url):
		if redis_data.get(url):
			return redis_data.get(url)
		else:
			longurl = getLongUrl(url)
			redis_data.set(url,longurl)
			return longurl
	else:
		return url



