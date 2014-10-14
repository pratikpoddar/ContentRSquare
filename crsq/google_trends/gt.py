from django.template.defaultfilters import slugify
from urlparse import urlparse
import json
import logging
import urllib2
from bs4 import BeautifulSoup
from crsq.crsqlib.stringutils import *

logger = logging.getLogger(__name__)

def get_top_trends(gurl):

	url = gurl+"/trends/hottrends/atom/feed"
	xml = urllib2.urlopen(url).read()
	xml = BeautifulSoup(xml, features="xml")
	return list(set(map(lambda x: slugify(crsq_unicode(x.title.text).replace('.com',' ').replace('.co.in',' ').replace('.org', ' ').replace('www.',' ').replace('.',' ')), xml.find_all('item'))))

def get_all_google_trends():
	return {'India': get_top_trends("http://www.google.co.in"), 'US': get_top_trends("http://www.google.com"), 'UK': get_top_trends("http://www.google.co.uk"), 'Australia': get_top_trends("http://www.google.com.au"), 'Spain': get_top_trends("http://www.google.es"), 'Brazil': get_top_trends("http://www.google.com.br"), 'Italy': get_top_trends("http://www.google.it"), 'France': get_top_trends("http://www.google.fr")}
	
