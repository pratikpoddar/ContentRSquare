import urllib
import pickledb

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



