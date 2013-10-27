#!/usr/bin/python
from __future__ import print_function
from alchemyapi import AlchemyAPI
import json
from get_twitter_graph import getStatus
import sys
import urllib
import urllib2
import re
from lxml import etree
from calais import Calais

alchemyapi = AlchemyAPI()
calais = Calais("rjfq8eq99bwum4fp3ncjafdw", submitter="python-calais-content-r-square")

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def get_Status_Concepts(status):
	response = alchemyapi.concepts('text', status)

	if response['status'] == 'OK':
		print('')
		print('## Concepts ##')
		for concept in response['concepts']:
			print(removeNonAscii('text: ' + concept['text'] + ' ' + concept['relevance']))
		return response['concepts']
	else:
		print('Error in concept tagging call: '+ response['statusInfo'])
		return None

def get_Status_Categories(status):
	response = alchemyapi.category('text',status)

	if response['status'] == 'OK':
		print('')
		print('## Category ##')
		print(removeNonAscii('text: '+ response['category'] + ' ' + response['score']))
		return response
	else:
		print('Error in text categorization call: '+ response['statusInfo'])
		return None

def get_Content_Analysis(status):
	
	url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20contentanalysis.analyze%20where%20text%3D%22" + urllib.quote_plus(re.compile('\W+').sub(' ', status).strip()) + "%22&diagnostics=true"
	root = etree.fromstring(urllib2.urlopen(url).read())
	relevantlist = root.getchildren()[1].getchildren()
	print('')
        print('## Yahoo Content Analysis ##')
	yresult = {}
	yresult['yentities'] = []
	yresult['ycategories'] = []
	for relevantgroup in relevantlist:
		if relevantgroup.tag == "{urn:yahoo:cap}entities":
			yresult['yentities'] = map(lambda entity: entity.getchildren()[0].text, relevantgroup)
		if relevantgroup.tag == "{urn:yahoo:cap}yctCategories":
			yresult['ycategories'] = map(lambda category: category.text, relevantgroup.getchildren())
	print(yresult)
	return yresult

def get_Calais_Topics(status):
	
	calais_result = calais.analyze(status)
	print('')
	print('## Open Calais Topics ##')
	try:
		print("Topics")
		calais_result.print_topics()
	except Exception as e:
		pass
	try:
		print("Entities")
		calais_result.print_entities()
	except Exception as e:
		pass
	return calais_result
	
if __name__ == "__main__":
	if len(sys.argv)>1:
		twitteridlist = [int(sys.argv[1])]
	else:
		twitteridlist = [66690578,62438757]

	calaisapires = None
	for twitterid in twitteridlist:
		statuses = getStatus(twitterid)
		concepts = get_Status_Concepts(statuses)
		categories = get_Status_Categories(statuses)
		yahooapires = get_Content_Analysis(statuses)
		calaisapires = get_Calais_Topics(statuses)



