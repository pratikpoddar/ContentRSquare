from elasticsearch import Elasticsearch
from crsq.models import ArticleInfo, ArticleTags
from urlparse import urlparse
import logging
from bs4 import BeautifulSoup
import math
from cluster import HierarchicalClustering
from Levenshtein import ratio as levenshtein_ratio

es = Elasticsearch()

# get trace logger and set level
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.DEBUG)

# add handlers to tracer
tracer.addHandler(logging.FileHandler('/mnt/dbmount/eslogs/debug.log'))

def createarticleindex():

	es.indices.create(
		index="article-index",
        	body={
          		'settings': {
				'analysis': {
					'analyzer': {
						'my_ngram_analyzer' : {
 					               	'tokenizer' : 'my_ngram_tokenizer',
							'filter': ['my_synonym_filter']
 	  					}
              				},
					'filter': {
						'my_synonym_filter': {
							'type': 'synonym',
							'format': 'wordnet',
							'synonyms_path': 'analysis/wn_s.pl'
						}
					},
	        			'tokenizer' : {
						'my_ngram_tokenizer' : {
					                'type' : 'nGram',
							'min_gram' : '1',
							'max_gram' : '50'
            					}
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
	res = es.index(index="article-index", doc_type='article', body=doc, id=articledict['url'])

	return

def deleteurl(url):
	
	try:
		es.delete(index="article-index", doc_type="article", id=url)
	except:
		pass

	return

def searchdoc(keywordstr, num=30, threshold=0.0, weightfrontloading=1.0, recencyweight=8.0, highlight=False):

	recency = recencyweight/1000000.0
	maxarticleid = str(100000.0)
        if keywordstr.strip()=='':
                return []

	if weightfrontloading== 1.0:
		keywordlist = keywordstr.split(' ')
		keywordstr = keywordstr
	else:
		keywordlist = keywordstr.split(' ')
		keywordpower = map(lambda y: 1+ (y**2-1)*(weightfrontloading-1)/(len(keywordlist)**2-1), sorted(range(1,(len(keywordlist))+1), key=lambda x: -x))
		keywordstr = ' '.join(map(lambda x: x[0]+"^"+str(x[1]), zip(keywordlist,keywordpower)))

        #res = es.search(index="article-index", fields="url", body={"query": {"query_string": {"query": keywordstr, "fields": ["text", "title", "tags", "domain"]}}})

	bodyquery = {
            "custom_score": {
                "script" : "_score * ("+str(1.0+recency)+"**(doc['articleid'].value*40000.0/"+maxarticleid+"))",
                "query": {
                        "query_string": {"query": keywordstr, "fields": ["text", "title", "tags", "domain"]}
                }
            }
        }

	if highlight==True:
	        res = es.search(index="article-index", size=max(num, 10), body={"query": bodyquery, "highlight" : {"fields" : {"*" : {}}}})
		urls = []
		for hit in res['hits']['hits']:
		    if hit['_score']>threshold:
			    url = hit["_source"]["url"]
			    highlight = list(set(map(lambda x: x.text.lower(), BeautifulSoup(' '.join(sum(hit['highlight'].values(), []))).find_all('em'))))
			    highlight_search = ' '.join(list(set(' '.join(filter(lambda x: x.lower() in highlight, keywordlist)).split())))
			    urls.append({'url':url, 'highlight': highlight_search})
		return urls

	else:
		res = es.search(index="article-index", fields="url", body={"query": bodyquery}, size=max(num,10))
		urls = []
		for hit in res['hits']['hits']:
		    if hit['_score']>threshold:
			    urls.append(hit["fields"]["url"])
			    if len(urls)==num:
				return urls
		return urls

def getall():
	res = es.search(index="article-index", body={"query": {"match_all": {}}}, size=500000, fields="")
        print("Getting all elements indexed - Got %d Hits" % res['hits']['total'])
	if res['hits']['total']>0:
		urls = map(lambda hit: hit["_id"], res['hits']['hits'])
	else:
		urls = []
        return urls

def indexurl(url):
	
	articledict = ArticleInfo.objects.filter(url=url).values()[0]
	tags = ' '.join(map(lambda x: x['tag'], ArticleTags.objects.filter(url=url).values('tag')))
	domain = urlparse(url)[1]
	if len(articledict) and len(tags)>0:
		indexdoc(dict(articledict.items() + [('tags', tags), ('domain', domain)]))
	return

def refreshdbtoes():

	dburls = map(lambda x:x ['url'], ArticleInfo.objects.all().values('url'))
	indexurls = getall()
	#for url in list(indexurls):
	#	deleteurl(url)
	#for url in list(dburls):
	#	indexurl(url)
	for url in list(set(indexurls)-set(dburls)):
		deleteurl(url)
	for url in list(set(dburls)-set(indexurls)):
		indexurl(url)

	return

def num_articles_search_exact(string):

	res = es.search(index="article-index", body={"query": {"query_string": {"query": '"' + string + '"', "fields": ["text", "title"]}}}, fields="", size=0)
	return res['hits']['total']

# Based on http://www2007.org/papers/paper632.pdf
def semantic_closeness_webdice(string1, string2):

	string1 = string1.lower()
	string2 = string2.lower()
	num1 = es.search(index="article-index", body={"query": {"query_string": {"query": '"' + string1 + '"', "fields": ["text", "title"]}}}, fields="", size=0)['hits']['total']
	num2 = es.search(index="article-index", body={"query": {"query_string": {"query": '"' + string2 + '"', "fields": ["text", "title"]}}}, fields="", size=0)['hits']['total']
	num12 = es.search(index="article-index", body={"query": {"query_string": {"query": '"' + string1 + '" AND "' + string2 + '"', "fields": ["text", "title"]}}}, fields="", size=0)['hits']['total']

	if float(num12)>30:
		ratio = 2.0*float(num12)/(float(num1)+float(num2))
		return math.atan(20.0*ratio)/(math.pi/2)

	else:
		return 0.0

def cluster_articles(urls, level=0.15):
	
	articles = map(lambda x: es.get(index="article-index", doc_type='article', id=x)['_source'], urls)
	print len(articles)
	#cl = HierarchicalClustering(articles, lambda x,y: 1.0-(2.0*float(len(list(set(x['tags'].split(' ')) & set(y['tags'].split(' ')))))/float((len(x['tags'].split(' ')) + len(y['tags'].split(' '))))))
	#cl = HierarchicalClustering(articles, lambda x,y: 100-(len(list(set(x['tags'].split(' ')) & set(y['tags'].split(' '))))))
	try:
		cl = HierarchicalClustering(articles, lambda x,y: 1-( levenshtein_ratio(' '.join(sorted(x['tags'])).lower(), ' '.join(sorted(y['tags'])).lower() ) ))
		clusters = cl.getlevel(level)
		urlclusters = []
		for clust in clusters:
			urlclusters.append(map(lambda x: x['url'], clust))
	
		return urlclusters
	except:
		return urls

