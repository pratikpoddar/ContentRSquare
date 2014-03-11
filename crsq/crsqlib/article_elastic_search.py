from elasticsearch import Elasticsearch
from crsq.models import *
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
		'domain': articledict['domain']
	}
	
	createarticleindex()
	res = es.index(index="article-index", doc_type='article', body=doc, id=articledict['url'])

	return

def searchdoc(keywordstr, num=30):
	res = es.search(index="article-index", body={"query": {"query_string": {"query": keywordstr, "fields": ["text", "title^2", "tags^3", "domain^3"]}}})
	print("Got %d Hits:" % res['hits']['total'])
	urls = []
	for hit in res['hits']['hits']:
	    urls.append(hit["_source"]["url"])
	    if len(urls)==num:
		return urls
	    #print("%(url)s: %(text)s" % hit["_source"])

	return urls

def indexurl(url):
	
	articledict = ArticleInfo.objects.filter(url=url).values()[0]
	tags = ' '.join(map(lambda x: x['tag'], ArticleTags.objects.filter(url=url).values('tag')))
	domain = urlparse(url)[1]
	if len(articledict):
		indexdoc(dict(articledict.items() + [('tags', tags), ('domain', domain)]))
	return

