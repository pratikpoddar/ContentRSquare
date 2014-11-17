from urlparse import urlparse
import json
import logging
import urllib2
import urllib
from bs4 import BeautifulSoup

def get_quora_page(topic):
        url = 'http://www.quora.com/search?q='+urllib.quote_plus(topic)
        return url



