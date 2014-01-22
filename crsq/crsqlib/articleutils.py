from goose import Goose
import urllib2
from crsq.crsqlib.text_summarize import text_summarize
import logging
from crsq.crsqlib import urlutils

logger = logging.getLogger(__name__)

def getArticleProperties(html):

	try:
		g = Goose()
		article = g.extract(raw_html=html)
	except:
		try:
			g = Goose({'enable_image_fetching':False})
			article = g.extract(raw_html=html)
		except:
			raise	

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
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
                opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), ('Accept-Charset', 'utf-8')]
		url = url.encode('utf-8')
		response = opener.open(url)
		if response.getcode() == 200:
			raw_html = response.read()
		else:
			raise
	except Exception as e:
		logger.exception('articleutils - getArticlePropertiesFromUrl - error getting article - ' + url + ' - ' + str(e))
		raise
	try:
		articledict = getArticleProperties(raw_html)
		articledict['url'] = urlutils.getCanonicalUrl(response.url)
	except Exception as e:
		logger.exception('articleutils - getArticlePropertiesFromUrl - error extracting article properties - ' + url + ' - ' + str(e))
		raise

	return articledict

def getArticleSemantics(html):

	tags = text_summarize.get_text_tags(html)
	topic = "Technology"
	summary = text_summarize.get_text_summary(html)

	return {'tags': tags, 'topic': topic, 'summary':summary}

