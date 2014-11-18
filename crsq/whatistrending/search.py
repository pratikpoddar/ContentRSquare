from urlparse import urlparse
import json
import logging
import urllib2
import urllib
from bs4 import BeautifulSoup
import simplejson
import re
import time
from cookielib import CookieJar
from functools32 import lru_cache

def get_quora_page(topic):
        url = 'http://www.quora.com/search?q='+urllib.quote_plus(topic)
        return url

def get_twitter_page(topic):
        url = 'https://twitter.com/search?q='+urllib.quote_plus(topic) +'&src=tren'
        return url

@lru_cache(maxsize=1024)
def get_twitter_handles_from_topic(topic):
        cj  = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent','Mozilla/5.0')]
        url = 'https://twitter.com/search?q=' + urllib.quote_plus(topic) + '&mode=users'
        html = opener.open(url).read()
        html = re.findall(r'<span class="username js-action-profile-name">(.*?)</span>',html)
        return html


        



