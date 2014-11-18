from django.template.defaultfilters import slugify
from urlparse import urlparse
import json
import logging
import urllib2
from bs4 import BeautifulSoup
from crsq.crsqlib.stringutils import *
from functools32 import lru_cache

@lru_cache(maxsize=1024)
def get_top_trends(regionID):

        url = 'http://gdata.youtube.com/feeds/api/standardfeeds/'+regionID+'/most_popular?v=2'
        xml = urllib2.urlopen(url).read()
        xml = BeautifulSoup(xml, features="xml")
        return map(lambda x: (crsq_unicode(x.title.text), crsq_unicode(x.player.attrs['url'])), xml.find_all('group'))

@lru_cache(maxsize=1024)
def get_all_youtube_trends():
        return {'India': get_top_trends("IN"), 'US': get_top_trends("US"), 'UK': get_top_trends("GB"), 'Australia': get_top_trends("AU"), 'Spain': get_top_trends("ES"), 'Brazil': get_top_trends("BR"), 'Italy': get_top_trends("IT"), 'France': get_top_trends("FR")}

