from elasticsearch import Elasticsearch
from crsq.models import *
from urlparse import urlparse

es = Elasticsearch()

def createemailindex():

	es.indices.create(
		index="email-index",
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

def indexemail(emaildict):

	doc = {
		'from': emaildict['emailfrom'],
		'cc' : emaildict['emailccto'],
		'bcc': emaildict['emailbccto'],
		'subject': emaildict['subject'],
		'body': emaildict['cleanbody'],
		'id' : emaildict['id']
	}
	
	createemailindex()
	res = es.index(index="email-index", doc_type='email', body=doc, id=emaildict['emailhash'])

	return

def searchemail(keywordstr, num=20):
	res = es.search(index="email-index", body={"query": {"query_string": {"query": keywordstr, "fields": ["from", "cc", "bcc", "subject^2", "body^3"]}}})
	print("Got %d Hits:" % res['hits']['total'])
	ids = []
	for hit in res['hits']['hits']:
	    ids.append(hit["_source"]["id"])
	    if len(ids)==num:
		return ids

	return ids

def indexemailid(emailhash):
	
	emaildict = EmailInfo.objects.filter(emailhash=emailhash).values()[0]
	if len(emaildict):
		indexemail(emaildict)
	return

