from elasticsearch import Elasticsearch
from crsq.models import ArticleInfo, ArticleTags, ArticleChanged
from urlparse import urlparse
import logging
from bs4 import BeautifulSoup
import math
import requests
import json
from django.conf import settings
es = Elasticsearch()

# get trace logger and set level
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.DEBUG)

# add handlers to tracer
tracer.addHandler(logging.FileHandler(settings.ES_LOGS+'debug.log'))

def createarticleindex():

	es.indices.create(
            index="article-index-2",
            body={
                    'settings': {
                            'analysis': {
                                    'analyzer': {
                                            'my_ngram_analyzer' : {
                                                    'tokenizer' : 'my_ngram_tokenizer',
                                                    'filter': ['my_filter', 'lowercase']
                                            }
                                    },
                                    'filter': {
                                            'my_filter': {
                                                    'type': 'edgeNGram',
                                                    'side': 'front',
                                                    'min_gram': '1',
                                                    'max_gram': '10'

                                            }
                                    },
                                    'tokenizer' : {
                                            'my_ngram_tokenizer' : {
                                                    'type' : 'nGram',
                                                    'min_gram' : '1',
                                                    'max_gram' : '10'
                                            }
                                    }
                            }
                    },
                    	'mappings': {
                        	'article': {
                                	'_all': {
                                    		'enabled': False
                                  	},
                                  	'_source': {
                                    		'compressed': True
                                  	},
                                  	'properties': {
                                    		'text': {'type': 'string', 'index': 'analyzed', 'analyzer': 'my_analyzer'},
                                                'title': {'type': 'string', 'index': 'analyzed', 'analyzer': 'my_analyzer'},
                                                'tags': {'type': 'string', 'index': 'analyzed', 'analyzer': 'my_analyzer'},
                                                'url': {'type': 'string', 'index': 'analyzed', 'analyzer': 'my_analyzer'},
                                                'domain': {'type': 'string', 'index': 'analyzed', 'analyzer': 'my_analyzer'},
                                  	}
                            	}
                    	}	
            },
            # ignore already existing index
            ignore=400
    	)
	return

def indexdoc(articledict):

	doc = {
		'text': articledict['articlecontent'],
		'title' : articledict['articletitle'],
		'url': articledict['url'],
		'tags': articledict['tags'],
		'domain': articledict['domain'],
		'articleid': articledict['id']
	}
	
	createarticleindex()
	res = es.index(index="article-index-2", doc_type='article', body=doc, id=articledict['url'])

	return

def deleteurl(url):
	
	try:
		es.delete(index="article-index-2", doc_type="article", id=url)
	except:
		pass

	return

def searchdoc(keywordstr, num=30, threshold=0.0, weightfrontloading=1.0, recencyweight=12.0, highlight=False):

	# weightfrontloading and highlight is not working

	recency = recencyweight/1000000.0
	maxarticleid = str(800000.0)
        if keywordstr.strip()=='':
                return []

	keywordstr = keywordstr

	bodyquery = {
            "custom_score": {
                "script" : "_score * ("+str(1.0+recency)+"**(doc['articleid'].value*20000.0/"+maxarticleid+"))",
                "query": {
                        "query_string": {"query": keywordstr, "fields": ["text", "title^4", "domain", "tags^3"]}
                }
            }
        }

	if highlight==True:
	        res = es.search(index="article-index-2", size=max(num, 10), body={"query": bodyquery, "highlight" : {"fields" : {"*" : {}}}})
		urls = []
		for hit in res['hits']['hits']:
		    if hit['_score']>threshold:
			    url = hit["_source"]["url"]
			    highlight = list(set(map(lambda x: x.text.lower(), BeautifulSoup(' '.join(sum(hit['highlight'].values(), []))).find_all('em'))))
			    highlight_search = ''
			    urls.append({'url':url, 'highlight': highlight_search})
		return urls

	else:
		res = es.search(index="article-index-2", fields="url", body={"query": bodyquery}, size=max(num,10))
		urls = []
		for hit in res['hits']['hits']:
		    if hit['_score']>threshold:
			    urls.append(hit["fields"]["url"])
			    if len(urls)==num:
				return urls
		return urls

def gettopterms():

	body = 	{
		"query" : {
			"match_all" : {  }
			},
		"facets" : {
			"tag" : {
				"terms" : {
					"field" : "tags",
					"size" : 40000
					}
				}
			}
	}

	res = es.search(index="article-index-2", body=body)
	return filter(lambda y: len(y)>=4, map(lambda x: x['term'], res['facets']['tag']['terms']))

def getall():
	res = es.search(index="article-index-2", body={"query": {"match_all": {}}}, size=500000, fields="")
        print("Getting all elements indexed - Got %d Hits" % res['hits']['total'])
	if res['hits']['total']>0:
		urls = map(lambda hit: hit["_id"], res['hits']['hits'])
	else:
		urls = []
        return urls

def indexurl(url):
	
	articledict = ArticleInfo.objects.filter(url=url).values()[0]
	tags = map(lambda x: x['tag'], ArticleTags.objects.filter(url=url).values('tag'))
	domain = urlparse(url)[1]
	if len(articledict) and len(tags)>0:
		indexdoc(dict(articledict.items() + [('tags', tags), ('domain', domain)]))
	return

def refreshdbtoes():

	urls = map(lambda x:x ['url'], ArticleChanged.objects.all().values('url'))
	urls = list(set(urls))
	for url in urls:
		if ArticleInfo.objects.filter(url=url).count()>0:
			try:
				deleteurl(url)
			except:	
				pass
			indexurl(url)
		else:
			try:
				deleteurl(url)
			except:
				pass
		ArticleChanged.objects.filter(url=url).delete()
	return

def force_refreshdbtoes():
	
	dburls = map(lambda x:x ['url'], ArticleInfo.objects.all().values('url'))
	indexurls = getall()
	for url in list(set(indexurls)-set(dburls)):
		deleteurl(url)
	for url in list(set(dburls)-set(indexurls)):
		indexurl(url)
	return

def num_articles_search_exact(string):

	res = es.search(index="article-index-2", body={"query": {"query_string": {"query": '"' + string + '"', "fields": ["text", "title"]}}}, fields="", size=0)
	return res['hits']['total']

# Based on http://www2007.org/papers/paper632.pdf
def semantic_closeness_webdice(string1, string2):

	string1 = string1.lower()
	string2 = string2.lower()
	num1 = es.search(index="article-index-2", body={"query": {"query_string": {"query": '"' + string1 + '"', "fields": ["text", "title"]}}}, fields="", size=0)['hits']['total']
	num2 = es.search(index="article-index-2", body={"query": {"query_string": {"query": '"' + string2 + '"', "fields": ["text", "title"]}}}, fields="", size=0)['hits']['total']
	num12 = es.search(index="article-index-2", body={"query": {"query_string": {"query": '"' + string1 + '" AND "' + string2 + '"', "fields": ["text", "title"]}}}, fields="", size=0)['hits']['total']

	if float(num12)>30:
		ratio = 2.0*float(num12)/(float(num1)+float(num2))
		return math.atan(20.0*ratio)/(math.pi/2)

	else:
		return 0.0

def searchdoc_clusters(urls, keywordstr):

	url = 'http://localhost:9200/article-index-2/article/_search_with_clusters?q=' + keywordstr + '&size=100&field_mapping_title=fields.title&field_mapping_content=fields.tags&fields=title,text,tags,url&algorithm=stc'
	clusters = json.loads(requests.get(url).text)['clusters']
	clusters = map(lambda x: x['documents'], filter(lambda x: not (x['label']=="Other Topics"), clusters))
	clusters = map(lambda x: filter(lambda y: y in urls, x), clusters)
	clusters = sorted(clusters, key=lambda x: -len(x))
	countedurls = []
	finalclusters = []
	for x in clusters:
		finalclusters.append(filter(lambda y: not y in countedurls, x))
		countedurls += x
	return filter(lambda x: len(x)>=2, finalclusters)

createarticleindex()

	
	

