import json
import jsonpickle
from crsq.crsqlib import urlutils, articleutils
import hashlib
from django.db.models import Max
import logging
from urlparse import urlparse

from crsq.models import TwitterListLinks, TwitterKeywordLinks, TweetLinks, ArticleInfo, ArticleSemantics, ArticleTags

logger = logging.getLogger(__name__)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def crsq_unicode(s):

        if s  == None:
                return s

        if isinstance(s, unicode):
                return s
        else:
                return s.decode('utf-8')


def put_article_details(url, source=None):
	url = urlutils.getCanonicalUrl(url)
	if ArticleInfo.objects.filter(url=url).count()==0:
		try:
			articledict = articleutils.getArticlePropertiesFromUrl(url)
			socialpower = urlutils.getSocialShares(url)
			articleinfo = ArticleInfo(url=urlutils.getCanonicalUrl(url), articletitle = crsq_unicode(articledict['title']), articleimage = crsq_unicode(articledict['image']), articlecontent = crsq_unicode(articledict['cleaned_text']), articledate = articledict['publish_date'], articlehtml = crsq_unicode(articledict['raw_html']), twitterpower= socialpower['tw'], fbpower = socialpower['fb'], source=source)
			if len(articledict['cleaned_text'].strip())>1:
				articleinfo.save()
		except Exception as e:
			logger.exception('articleutilsdb - put_article_details - error saving article - ' + removeNonAscii(url) + ' - ' + str(e))
	return

def put_article_semantics_tags(url):
	url = urlutils.getCanonicalUrl(url)
	if ArticleInfo.objects.filter(url=url).count()==0:
		return
	if ArticleSemantics.objects.filter(url=url).count()==0 or ArticleTags.objects.filter(url=url).count()==0:
		try:
			content = crsq_unicode(ArticleInfo.objects.filter(url=url).values('articlecontent')[0]['articlecontent'])
			semantics_dict = articleutils.getArticleSemanticsTags(content)
			semantics_row = ArticleSemantics(url=urlutils.getCanonicalUrl(url), summary = crsq_unicode(semantics_dict['summary']), topic = crsq_unicode(semantics_dict['topic']))
			if ArticleSemantics.objects.filter(url=url).count()==0:
				semantics_row.save()
			if ArticleTags.objects.filter(url=url).count()==0:
				for tag in semantics_dict['tags']:
					tag_row = ArticleTags(url=url, tag=crsq_unicode(tag))
					if ArticleTags.objects.filter(url=url, tag=crsq_unicode(tag)).count()==0:
						tag_row.save()
		except Exception as e:
			logger.exception('articleutilsdb - put_article_semantics_tags - error getting article semantics / tags - ' + removeNonAscii(url) + ' - ' + str(e))

	return

