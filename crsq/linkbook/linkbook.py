import json
import jsonpickle
from time import sleep
import sys
import itertools
from crsq.crsqlib import urlutils, articleutils
import hashlib
from django.db.models import Max
import logging
from urlparse import urlparse
from bs4 import BeautifulSoup

from crsq.models import TwitterListLinks, TwitterKeywordLinks, TweetLinks, ArticleInfo, ArticleSemantics, ArticleTags

logger = logging.getLogger(__name__)

def get_articles(sector, location):
	articles = ArticleInfo.objects.exclude(articlehtml=None).exclude(articlehtml='').order_by('-time').values()
	return filter(lambda x: len(x['articlecontent'])>300, articles)

def get_linkbook_articles(sharer, topic):

        articles = get_articles("technology", "world")[:10]
	articles = map(lambda x: dict( x, **{'domain': urlparse.urlparse(x['url'])[1]}), articles)
	articles = map(lambda x: dict( x, **{'preloads': sum(articleutils.getArticlePreloads(x['articlehtml']).values(),[]) }), articles)
	return articles

