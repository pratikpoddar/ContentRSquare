from goose import Goose
import urllib2
from crsq.crsqlib.text_summarize import text_summarize
from crsq.crsqlib.wikianalytics import wikiutils

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

	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	response = opener.open(url)
	raw_html = response.read()
	articledict = getArticleProperties(raw_html)
	articledict['url'] = url
	return articledict

def getArticleCategoryFromProperty(articleProperty):

	text = articleProperty['cleaned_text']
	tags = []
	try:
		tags += text_summarize.get_nltk_ne(text)
	except:
		pass

        try:
                tags += text_summarize.get_python_tagger(text)
        except:
                pass

        try:
                tags += text_summarize.get_topia_termextract(text)
        except:
                pass

	tags = filter(lambda x: x['freebase'] != None, tags)
	wikitags = map(lambda x: x['freebase'], tags)
	wikitags = filter(lambda x: x['wikilink']!='', wikitags)
	wikitags = map(lambda x: x['wikilink'], wikitags)
	wikitags = filter(lambda x: x[0:4]=="/en/", wikitags)

	wikicategories = map(lambda x: wikiutils.get_wiki_categories(x), wikitags)
	
	return wikicategories

	
	





	



