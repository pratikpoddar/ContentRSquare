from goose import Goose
import urllib2
from crsq.crsqlib.text_summarize import text_summarize
import logging
from crsq.crsqlib import urlutils

logger = logging.getLogger(__name__)

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def getArticleProperties(html):
	
	try:
		html = html.encode('utf-8')
	except:
		html = removeNonAscii(html)
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
		articledict['cleaned_text'] = article.cleaned_text.encode('utf-8')
	except:
		articledict['cleaned_text'] = None
	try:
		articledict['domain'] = article.domain
	except:
		articledict['domain'] = None

	try:
		articledict['final_url'] = article.final_url
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
		if articledict['image'].find('http') != 0:
			raise
	except:
		articledict['image'] = None

	articledict['url'] = None

	return articledict

def getArticlePropertiesFromUrl(url):

	try:
		raw_html = ''
		respurl = ''

                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
                url = url.encode('utf-8')
                try:
                        resp = opener.open(url)
                        if resp.getcode() == 200:
	                        raw_html = resp.read()
        	                respurl = resp.url
                except urllib2.HTTPError as err:
                        if err.code == 403:
                                opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11 Chrome/32.0.1700.77 Safari/537.36'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), ('Accept-Charset', 'utf-8')]
                                resp = opener.open(url)
                                if resp.getcode() == 200:
					raw_html = resp.read()
		                        respurl = resp.url
			else:
				raise
		except Exception as e:
			raise

		if raw_html == '':
			raise

	except Exception as e:
		logger.exception('articleutils - getArticlePropertiesFromUrl - error getting article - ' + url + ' - ' + str(e))
		raise
	try:
		articledict = getArticleProperties(raw_html)
		articledict['url'] = urlutils.getCanonicalUrl(respurl)
	except Exception as e:
		logger.exception('articleutils - getArticlePropertiesFromUrl - error extracting article properties - ' + url + ' - ' + str(e))
		raise

	return articledict

def getArticleSemanticsTags(text):

	text = text.encode('utf-8')
	tags = text_summarize.get_text_tags(text)
	topic = text_summarize.get_text_topic(text)
	summary = text_summarize.get_text_summary(text)

	return {'tags': tags, 'topic': topic, 'summary':summary }

