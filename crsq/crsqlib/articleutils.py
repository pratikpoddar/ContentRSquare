from goose import Goose
import urllib2
from crsq.crsqlib.text_summarize import text_summarize
import logging

logger = logging.getLogger(__name__)

def getArticleProperties(html):

	g = Goose()
	article = g.extract(raw_html=html)

	articledict = {}
	try:
		articledict['canonical_link'] = article.canonical_link
	except:
		articledict['canonical_link'] = None
	try:
		articledict['cleaned_text'] = article.cleaned_text
	except:
		articledict['cleaned_text'] = None
	try:
		articledict['domain'] = article.domain
	except:
		articledict['domain'] = None

	try:
		articledict['final_url'] = articledict.final_url
	except:
		articledict['final_url'] = None

	try:
		articledict['meta_description'] = article.meta_description
	except:
		articledict['meta_description'] = None

	try:
		articledict['meta_keywords'] = article.meta_keywords
	except:
		articledict['meta_keywords'] = None

	try:
		articledict['publish_date'] = article.publish_date
	except:
		articledict['publish_date'] = None
	
	try:
		articledict['title'] = article.title
	except:
		articledict['title'] = None

	try:
		articledict['image'] = article.top_image.src
	except:
		articledict['image'] = None

	articledict['url'] = None

	return articledict

def getArticlePropertiesFromUrl(url):

	try:
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		response = opener.open(url)
		raw_html = response.read()
	except Exception as e:
		logger.exception('articleutils - getArticlePropertiesFromUrl - error getting article - ' + url + ' - ' + str(e))
		raise
	try:
		articledict = getArticleProperties(raw_html)
		articledict['url'] = url
	except Exception as e:
		logger.exception('articleutils - getArticlePropertiesFromUrl - error extracting article properties - ' + url + ' - ' + str(e))
		raise

	return articledict
	
