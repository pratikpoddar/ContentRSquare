from urlparse import urlparse
import json
import logging
import urllib2
import urllib
from bs4 import BeautifulSoup
from crsq.crsqlib.stringutils import *

def get_questions(topic):

        url = 'http://www.quora.com/search?q='+topic
        text = urllib2.urlopen(url).read()
        soup = BeautifulSoup(text)
        elems = soup.find_all(class_='title')
	return map(lambda x: x.text, elems)

