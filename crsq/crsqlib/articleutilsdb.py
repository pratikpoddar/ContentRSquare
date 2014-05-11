import json
import jsonpickle
from crsq.crsqlib import urlutils, articleutils
from crsq.crsqlib.stringutils import *
import hashlib
from django.db.models import Max
import logging
from urlparse import urlparse
import hashlib
import langid
import re

from crsq.models import TwitterListLinks, TwitterKeywordLinks, TweetLinks, ArticleInfo, ArticleSemantics, ArticleTags, DeleteLinks

langid.langid.load_model()

logger = logging.getLogger(__name__)

langid_identifier = langid.langid.identifier

def put_article_details(url, source=None):
	url = urlutils.getCanonicalUrl(url)
	if ArticleInfo.objects.filter(url=url).count()==0:
		try:
			articledict = articleutils.getArticlePropertiesFromUrl(url)
			socialpower = urlutils.getSocialShares(url)
			articleinfo = ArticleInfo(url=urlutils.getCanonicalUrl(url), articletitle = crsq_unicode(articledict['title']), articleimage = crsq_unicode(articledict['image']), articlecontent = crsq_unicode(articledict['cleaned_text']), articledate = articledict['publish_date'], articlehtml = crsq_unicode(articledict['raw_html']), twitterpower= socialpower['tw'], fbpower = socialpower['fb'], source=source)
			if len(articledict['cleaned_text'].strip())>250:
				if ArticleInfo.objects.filter(contenthash=str(int(hashlib.md5(removeNonAscii(crsq_unicode(articledict['cleaned_text']))).hexdigest(), 16))).count()==0:
					try:
						if langid_identifier.classify( re.match(r'(?:[^.:]*[.:]){2}', removeNonAscii(crsq_unicode(articledict['cleaned_text']))).group() )[0]=='en':
							articleinfo.save()
						else:
							try:
								dl = DeleteLinks(url=url, reason="Not english text")
								dl.save()
							except:
								pass
					except:
						articleinfo.save()
			else:
				try:
					dl = DeleteLinks(url=url, reason="Article Clean Text is less than 250 chars")
					dl.save()
				except:
					pass
		except Exception as e:
			try:
				if str(e).find('Read timed out. (read timeout=8)')>-1:
					dl = DeleteLinks(url=url, reason="Time out")
                                        dl.save()
			except:
				pass
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

