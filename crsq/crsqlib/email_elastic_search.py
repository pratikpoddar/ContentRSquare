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
		'to': emaildict['emailto'],
		'cc' : emaildict['emailccto'],
		'bcc': emaildict['emailbccto'],
		'subject': emaildict['subject'],
		'body': emaildict['cleanbody'].replace('@',' ').replace('gmail.com', ''),
		'messageid': emaildict['messageid'],
		'emailhash': emaildict['emailhash'],
	}
	
	createemailindex()
	res = es.index(index="email-index", doc_type='email', body=doc, id=emaildict['emailhash'])

	return

def deleteemailhash(emailhash):

        try:
                es.delete(index="email-index", doc_type="email", id=emailhash)
        except:
                pass

        return

def searchemail(keywordstr, num=20):

	if keywordstr.strip()=='':
		return []

	#res = es.search(index="email-index", body={"query": {"query_string": {"query": keywordstr, "fields": ["from", "to", "cc", "bcc", "subject^2", "body^3"]}}})

        res = es.search(index="email-index", fields="url", body={"query": {
            "custom_score": {
                "script" : "_score",
                "query": {
                        "query_string": {"query": keywordstr, "fields": ["from", "to", "cc", "bcc", "subject^2", "body^3"]}
                },
            }
        }
        })

	ids = []
	for hit in res['hits']['hits']:
	    ids.append(hit["_source"]["messageid"])
	    if len(ids)==num:
		return ids

	return ids

def indexemailhash(emailhash):
	
	emaildict = EmailInfo.objects.filter(emailhash=emailhash).values()[0]
	if len(emaildict):
		indexemail(emaildict)
	return

def recommendedemails(emailhash):

	res = es.mlt(index="email-index", doc_type="email", body={"query": {"query_string": {"query": "\*", "fields": ["from", "cc", "bcc", "subject^2", "body^3"]}}}, id=emailhash, percent_terms_to_match=0.1)
        if res['hits']['total']>0:
                emailhashes = map(lambda hit: hit["_id"], res['hits']['hits'])
        else:
                emailhashes = []
        return emailhashes

def getall():
	res = es.search(index="email-index", body={"query": {"match_all": {}}}, size=100000, fields="emailhash")
        print("Getting all indices -  %d Hits:" % res['hits']['total'])
	if res['hits']['total']>0:
		emailhashes = map(lambda hit: hit["fields"]["emailhash"], res['hits']['hits'])
	else:
		emailhashes = []
        return emailhashes

def refreshdbtoes():
	
	dbhashes = map(lambda x:x ['emailhash'], EmailInfo.objects.all().values('emailhash'))
	indexhashes = getall()
	#for h in list(indexhashes):
	#	deleteemailhash(h)
	#for h in list(dbhashes):
	#	indexemailhash(h)
	for h in list(set(indexhashes)-set(dbhashes)):
		deleteemailhash(h)
	for h in list(set(dbhashes)-set(indexhashes)):
		indexemailhash(h)

	return


