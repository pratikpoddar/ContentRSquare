from crsq.models import ArticleInfo, ArticleSemantics, ArticleTags
from urlparse import urlparse

def get_article_json(url):

	try:
		article = ArticleInfo.objects.filter(url=url).values()
		articlesemantics = ArticleSemantics.objects.filter(url=url).values()
		json_object = {}
		try:
			json_object['startDate'] = article['publish_date']
		except:
			json_object['startDate'] = "2012,12,11"
		try:
			json_object['endDate'] = article['publish_date']+1
		except:
			pass
		json_obejct['headline'] = article['articletitle']
		json_object['text'] = articlesemantics['summary']
		json_object['asset'] = { "media": article['articlemage'], "credit": urlparse(url)[1], "caption":""}

		return json_object
	except:
		return None

def get_timeline_json(urllist):
	
	output = {}
	output['timeline'] = {}
	output['timeline']['headline'] = "The Main Timeline Headline Goes here"
	output['timeline']['type'] = 'default'
	output['timeline']['text'] = "<p>Intro body text goes here, some HTML is ok</p>"
	output['timeline']['asset'] = {  "media":"", "credit":"Credit Name Goes Here", "caption":"Caption text goes here"}
	output['timeline']['date'] = filter(lambda x: x, map(lambda x: get_article_json(x) , urllist))
	
	return output




	
	
	
