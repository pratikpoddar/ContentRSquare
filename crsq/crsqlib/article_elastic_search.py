from elasticsearch import Elasticsearch
from crsq.models import ArticleInfo

es = Elasticsearch()

def indexdoc(articledict):

	doc = {
		'text': articledict['articlecontent'],
		'title' : articledict['articletitle'],
		'url': articledict['url']
	}
	
	res = es.index(index="article-index", doc_type='article', body=doc, id=articledict['url'])


def searchdoc(keywordstr):
	res = es.search(index="article-index", body={"query": {"query_string": {"query": keywordstr, "fields": ["text", "title"]}}})
	print("Got %d Hits:" % res['hits']['total'])
	for hit in res['hits']['hits']:
	    print("%(url)s: %(text)s" % hit["_source"])

def indexurl(url):
	
	articledict = ArticleInfo.objects.filter(url=url).values()
	if len(articledict):
		indexdoc(articledict)
	return

