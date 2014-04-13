from elasticsearch import Elasticsearch
from crsq.models import ArticleInfo, ArticleTags
from urlparse import urlparse
import logging
from bs4 import BeautifulSoup

es = Elasticsearch()

# get trace logger and set level
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.DEBUG)

# add handlers to tracer
tracer.addHandler(logging.FileHandler('/var/log/elasticsearch/debug.log'))

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

	recency = recencyweight/1000000
	maxarticleid = str(100000)
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
                "script" : "_score * ("+str(1.0+recency)+"**(doc['articleid'].value*40000/"+maxarticleid+"))",
                "query": {
                        "query_string": {"query": keywordstr, "fields": ["text", "title", "tags", "domain"]}
                }
            }
        }

	if highlight==True:
	        res = es.search(index="article-index", body={"query": bodyquery, "highlight" : {"fields" : {"*" : {}}}})
		urls = []
		for hit in res['hits']['hits']:
		    if hit['_score']>threshold:
			    url = hit["_source"]["url"]
			    highlight = list(set(map(lambda x: x.text.lower(), BeautifulSoup(' '.join(sum(hit['highlight'].values(), []))).find_all('em'))))
			    highlight_search = ' '.join(list(set(' '.join(filter(lambda x: x.lower() in highlight, keywordlist)).split())))
			    urls.append({'url':url, 'highlight': highlight_search})
		return urls

	else:
		res = es.search(index="article-index", fields="url", body={"query": bodyquery})
		urls = []
		for hit in res['hits']['hits']:
		    if hit['_score']>threshold:
			    urls.append(hit["fields"]["url"])
			    if len(urls)==num:
				return urls
		return urls

def getall():
	res = es.search(index="article-index", body={"query": {"match_all": {}}}, size=100000, fields="")
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

	res = es.search(index="article-index", body={"query": {"query_string": {"query": '"' + string + '"', "fields": ["text", "title"]}}}, fields="")
	return res['hits']['total']

