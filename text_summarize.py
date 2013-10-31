#!/usr/bin/python
from __future__ import print_function
from alchemyapi import AlchemyAPI
import json
import sys
import urllib
import urllib2
import re
from lxml import etree
from calais import Calais

alchemyapi = AlchemyAPI()
calais = Calais("rjfq8eq99bwum4fp3ncjafdw", submitter="python-calais-content-r-square")

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def get_Text_Concepts(text):
	response = alchemyapi.concepts('text', text)

	if response['status'] == 'OK':
		print('')
		print('## Concepts ##')
		responseOutput = []
		for concept in response['concepts']:
			print(removeNonAscii('text: ' + concept['text'] + ' ' + concept['relevance']))
			responseOutput.append({'text': concept['text'], 'freebase': get_Freebase_Meaning(concept['text']), 'source': "get_Text_Concepts"})
		return responseOutput
	else:
		print('Error in concept tagging call: '+ response['statusInfo'])
		return None

def get_Text_Categories(text):
	response = alchemyapi.category('text',text)

	if response['status'] == 'OK':
		print('')
		print('## Category ##')
		responseOutput = {}
		print(removeNonAscii('text: '+ response['category'] + ' ' + response['score']))
		if response['category'] == "unknown":
			responseOutput = None
		else:
			responseOutput = {'text': response['category'], 'freebase': get_Freebase_Meaning(response['category']), 'source': "get_Text_Categories" }
		return responseOutput
	else:
		print('Error in text categorization call: '+ response['statusInfo'])
		return None

def get_Content_Analysis(text):
	
	url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20contentanalysis.analyze%20where%20text%3D%22" + urllib.quote_plus(re.compile('\W+').sub(' ', text).strip()) + "%22&diagnostics=true"
	root = etree.fromstring(urllib2.urlopen(url).read())
	relevantlist = root.getchildren()[1].getchildren()
	print('')
        print('## Yahoo Content Analysis ##')
	yresult = {}
	responseOutput = []
	yresult['yentities'] = []
	yresult['ycategories'] = []
	for relevantgroup in relevantlist:
		if relevantgroup.tag == "{urn:yahoo:cap}entities":
			yresult['yentities'] = map(lambda entity: entity.getchildren()[0].text, relevantgroup)
			responseOutput += map(lambda x: {'text': x, 'freebase': get_Freebase_Meaning(x), 'source':'yentities'}, yresult['yentities'])
		if relevantgroup.tag == "{urn:yahoo:cap}yctCategories":
			yresult['ycategories'] = map(lambda category: category.text, relevantgroup.getchildren())
			responseOutput += map(lambda x: {'text': x, 'freebase': get_Freebase_Meaning(x), 'source':'ycategories'}, yresult['ycategories'])
	print(responseOutput)
	return responseOutput

def get_Calais_Topics(text):
	
	calais_result = calais.analyze(text)
	print('')
	print('## Open Calais ##')
	responseOutput = []
	try:
		print("Calais Topics")
		calais_result.print_topics()
		responseOutput += map(lambda x: {'text': x['name'], 'source': 'calais_topics', 'freebase': get_Freebase_Meaning(x['name'])}, calais_result.topics)
	except Exception as e:
		pass

	try:
		print("Calais Entities")
		calais_result.print_entities()
		responseOutput += map(lambda x: {'text': x['name'], 'source': 'calais_entities', 'freebase': get_Freebase_Meaning(x['name'])}, calais_result.entities)
	except Exception as e:
		pass
	
	responseOutput = filter(lambda x: x['freebase'] != None, responseOutput)
	return responseOutput

def get_Freebase_Meaning(term):
	
	try:
		term = removeNonAscii(term)
		url = "https://www.googleapis.com/freebase/v1/search?query=" + urllib.quote_plus(term)
		jsonResult = json.loads(urllib2.urlopen(url).read())['result']
		if jsonResult[0]['score']>100:
			try:
				return {'parentnode': jsonResult[0]['notable']['name'], 'wikilink': jsonResult[0]['id']}
			except:
				try:
					return {'parentnode': '', 'wikilink': jsonResult[0]['id']}
				except:
					return {'parentnode': jsonResult[0]['notable']['name'], 'wikilink': ''}
		else:
			return None
	except Exception as e:
		return None
	
if __name__ == "__main__":
	from get_twitter_graph import getStatus
	if len(sys.argv)>1:
		twitteridlist = [int(sys.argv[1])]
	else:
		twitteridlist = [66690578,62438757]
		twitteridlist = [66690578]

	for twitterid in twitteridlist:
		statuses = getStatus(twitterid)
		concepts = get_Text_Concepts(statuses)
		categories = get_Text_Categories(statuses)
		yahooapires = get_Content_Analysis(statuses)
		calaisapires = get_Calais_Topics(statuses
)



