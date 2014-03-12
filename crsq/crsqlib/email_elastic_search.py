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

	res = es.search(index="email-index", body={"query": {"query_string": {"query": keywordstr, "fields": ["from", "cc", "bcc", "subject^2", "body^3"]}}})
	print("Got %d Hits:" % res['hits']['total'])
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
	
	messageid = EmailInfo.objects.get(emailhash=emailhash).messageid
	emailtags = ' '.join(map(lambda x: x['tag'], EmailTags.objects.filter(messageid=messageid).values('tag')))
	emailtags = emailtags.replace('-', ' ').title()
	return searchemail(emailtags, 5)

def getall():
	res = es.search(index="email-index", body={"query": {"match_all": {}}}, size=100000, fields="emailhash")
        print("Got %d Hits:" % res['hits']['total'])
	if res['hits']['total']>0:
		emailhashes = map(lambda hit: hit["fields"]["emailhash"], res['hits']['hits'])
	else:
		emailhashes = []
        return emailhashes

def refreshdbtoes():
	
	dbhashes = map(lambda x:x ['emailhash'], EmailInfo.objects.all().values('emailhash'))
	indexhashes = getall()
	for h in list(set(indexhashes)-set(dbhashes)):
		deleteemailhash(h)
	for h in list(set(dbhashes)-set(indexhashes)):
		indexemailhash(h)

	return

