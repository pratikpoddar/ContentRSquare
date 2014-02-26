from crsq.crsqlib.goose import Goose
import urllib2
from crsq.crsqlib.text_summarize import text_summarize
import logging
from crsq.crsqlib import urlutils
from cookielib import CookieJar
from bs4 import BeautifulSoup
import re
from django.template.defaultfilters import slugify
import requests

logger = logging.getLogger(__name__)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def crsq_unicode(s):
	
	if s  == None:
		return s

        if isinstance(s, unicode):
                return s
        else:
                return s.decode('utf-8')

def getArticleProperties(html):
	
	html = crsq_unicode(html)
	
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
		articledict['canonical_link'] = crsq_unicode(article.canonical_link)
	except Exception as e:
		logger.exception('articleutils - getArticleProperties - error getting article - ' + removeNonAscii(html) + ' - ' + str(e))
		articledict['canonical_link'] = None
	try:
		articledict['cleaned_text'] = crsq_unicode(article.cleaned_text)
	except Exception as e:
		logger.exception('articleutils - getArticleProperties - error getting article - ' + removeNonAscii(html) + ' - ' + str(e))
		articledict['cleaned_text'] = None
	try:
		articledict['domain'] = crsq_unicode(article.domain)
	except Exception as e:
		logger.exception('articleutils - getArticleProperties - error getting article - ' + removeNonAscii(html) + ' - ' + str(e))
		articledict['domain'] = None

	try:
		articledict['final_url'] = urlutils.getCanonicalUrl(crsq_unicode(article.final_url))
	except Exception as e:
		logger.exception('articleutils - getArticleProperties - error getting article - ' + removeNonAscii(html) + ' - ' + str(e))
		articledict['final_url'] = None

	try:
		articledict['meta_description'] = crsq_unicode(article.meta_description)
	except Exception as e:
		logger.exception('articleutils - getArticleProperties - error getting article - ' + removeNonAscii(html) + ' - ' + str(e))
		articledict['meta_description'] = None

	try:
		articledict['meta_keywords'] = None
	except Exception as e:
		logger.exception('articleutils - getArticleProperties - error getting article - ' + removeNonAscii(html) + ' - ' + str(e))
		articledict['meta_keywords'] = None

	try:
		articledict['publish_date'] = article.publish_date
	except Exception as e:
		logger.exception('articleutils - getArticleProperties - error getting article - ' + removeNonAscii(html) + ' - ' + str(e))
		articledict['publish_date'] = None
	
	try:
		articledict['title'] = crsq_unicode(article.title)
	except Exception as e:
		logger.exception('articleutils - getArticleProperties - error getting article - ' + removeNonAscii(html) + ' - ' + str(e))
		articledict['title'] = None

	try:
		articledict['image'] = article.top_image.src
		if articledict['image'].find('http') != 0:
			raise
	except:
		articledict['image'] = None

	try:
		articledict['raw_html'] = crsq_unicode(article.raw_html)
	except Exception as e:
		logger.exception('articleutils - getArticleProperties - error getting article - ' + removeNonAscii(html) + ' - ' + str(e))
		articledict['raw_html'] = None

	articledict['url'] = None

	return articledict

def getArticlePreloads(html):
	
	html = crsq_unicode(html)
        bs = BeautifulSoup(html)
	preload = {}
	preload['js'] = []
	preload['css'] = []
	preload['img'] = []
        jss = bs.find_all(name = 'script', attrs = { 'src': re.compile('^http:|^https:') })
	for js in jss:
		if js['src'].find('doubleclick') == -1:
			preload['js'].append(js['src'])
        csss = bs.find_all(name = 'link', attrs = { 'type': 'text/css', 'href': re.compile('^http:|^https:') })
	for css in csss:
		if css['href'].find('doubleclick') == -1:
			preload['css'].append(css['href'])
        imgs = bs.find_all(name = 'img', attrs = { 'src': re.compile('^http:|^https:')})
	for img in imgs:
		if img['src'].find('doubleclick') == -1:
			preload['img'].append(img['src'])
	
	return preload

def getArticlePropertiesFromUrl(url):

	try:
                url = urlutils.getCanonicalUrl(crsq_unicode(url))
                r = requests.get(url, timeout=8)
		raw_html = crsq_unicode(r.text)
		respurl = urlutils.getCanonicalUrl(crsq_unicode(r.url))
		raw_html = raw_html.replace(crsq_unicode('&nbsp;'), crsq_unicode(' '))
		raw_html = raw_html.replace(crsq_unicode('\xc2\xa0'), crsq_unicode(' '))
		articledict = getArticleProperties(raw_html)
		articledict['url'] = urlutils.getCanonicalUrl(respurl)
	except Exception as e:
		logger.exception('articleutils - getArticlePropertiesFromUrl - error extracting article properties - ' + url + ' - ' + str(e))
		raise

	return articledict

def getArticleSemanticsTags(text):

	text = crsq_unicode(text)
	tags = map(lambda x: crsq_unicode(slugify(x)), text_summarize.get_text_tags(text))
	#topic = crsq_unicode(text_summarize.get_text_topic(text))
	topic = ''

	try:
		summary = crsq_unicode(text_summarize.get_text_summary(text))
	except:
		summary = ''

	return {'tags': tags, 'topic': topic, 'summary':summary }

