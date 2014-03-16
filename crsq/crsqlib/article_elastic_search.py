from elasticsearch import Elasticsearch
from crsq.models import ArticleInfo, ArticleTags
from urlparse import urlparse

es = Elasticsearch()

def createarticleindex():

	es.indices.create(
		index="article-index",
        	body={
          		'settings': {
				'analysis': {
					'analyzer': {
						'my_ngram_analyzer' : {
 					               	'tokenizer' : 'my_ngram_tokenizer'
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

def searchdoc(keywordstr, num=30):

        if keywordstr.strip()=='':
                return []

	#res = es.search(index="article-index", fields="url", body={"query": {"query_string": {"query": keywordstr, "fields": ["text", "title", "tags", "domain"]}}})

        res = es.search(index="article-index", fields="url", body={"query": {
            "custom_score": {
                "script" : "_score * (1.00003**doc['articleid'].value)",
                "query": {
                	"query_string": {"query": keywordstr, "fields": ["text", "title", "tags", "domain"]}
                },

            }
        }
        })

	urls = []
	for hit in res['hits']['hits']:
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
	if len(articledict):
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

