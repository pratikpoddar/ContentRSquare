#!/usr/bin/python
from __future__ import print_function
from alchemyapi_python.alchemyapi import AlchemyAPI
import json
import sys
import urllib
import urllib2
import re
from lxml import etree
from calais import Calais
import nltk
from tagger import tagger
import pickle

alchemyapi = AlchemyAPI()
calais = Calais("rjfq8eq99bwum4fp3ncjafdw", submitter="python-calais-content-r-square")

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def get_python_tagger(text):

        print('')
        print ('## Python Tagger ##')
	weights = pickle.load(open('text_summarize/tagger/data/dict.pkl', 'rb')) 
	myreader = tagger.Reader()
	mystemmer = tagger.Stemmer()
	myrater = tagger.Rater(weights)
	mytagger = tagger.Tagger(myreader, mystemmer, myrater)
	tags = list(mytagger(text, 5))

        responseOutput = []
	print(tags)
        for tag in tags:
		try:
	                responseOutput.append({'text': str(tag), 'freebase': get_Freebase_Meaning(str(tag)), 'source': "get_python_tagger"})
		except Exception as e:
			print('Error in Python Tagger: ' + str(e))

        responseOutput = filter(lambda x: x['freebase'] != None, responseOutput)
        try:
                print(responseOutput)
        except:
                pass
        return responseOutput
	

def get_nltk_ne(text):

	print('')
	print ('## NLTK NE ##')
        tags = nltk.pos_tag(nltk.word_tokenize(text))
        ne = nltk.ne_chunk(tags, binary=True)
        list_of_nes = []
        for i in range(len(ne)):
                try:
                        if (ne[i].node=="NE"):
                                list_of_nes.append(' '.join(map(lambda x: x[0], ne[i].leaves())))
                except:
                        pass

        list_of_nes = filter(lambda x: len(x)>4, list_of_nes)

        responseOutput = []

        for ne in list_of_nes:
                responseOutput.append({'text': ne, 'freebase': get_Freebase_Meaning(ne), 'source': "get_nltk_ne"})

        responseOutput = filter(lambda x: x['freebase'] != None, responseOutput)
        try:
                print(responseOutput)
        except:
                pass
        return responseOutput

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
		print('Error in Alchemy concept tagging call: '+ response['statusInfo'])
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
		print('Error in Alchemy text categorization call: '+ response['statusInfo'])
		return None

def get_Content_Analysis(text):
	
	url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20contentanalysis.analyze%20where%20text%3D%22" + urllib.quote_plus(re.compile('\W+').sub(' ', text).strip()) + "%22&diagnostics=true"

	try:
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
	except Exception as e:
		print('Error in Yahoo Content Analysis: ' + str(e))
		

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
		print('Error in Calais Topics Extraction ' + str(e))
		pass

	try:
		print("Calais Entities")
		calais_result.print_entities()
		responseOutput += map(lambda x: {'text': x['name'], 'source': 'calais_entities', 'freebase': get_Freebase_Meaning(x['name'])}, calais_result.entities)
	except Exception as e:
		print('Error in Calais Entities Extraction ' + str(e))
		pass
	
	#responseOutput = filter(lambda x: x['freebase'] != None, responseOutput)
	print(responseOutput)
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
		print('Error in Freebase Meaning ' + str(term) + ' : ' + str(e))
		return None

if __name__=="__main__":	
	text = "In a shake up ahead of the LS polls, environment minister Jayanthi Natarajan resigned from the Union council of ministers. More resignations may be in line for being drafted into party work. The resignation of 59-year-old Natarajan, minister of state with independent charge of environment and forests, has been accepted by the President, a Rashtrapati Bhavan communique said. It also said that oil minister M Veerappa Moily will hold additional charge of the environment ministry. Natarajan, a senior member of Rajya Sabha doing a third term, hails from Tamil Nadu and was brought into the ministry two years ago. Sources said Natarajan, who has, of late, been more visible on television channels defending the party, may be drafted for organisation work. Sources said there could be some more ministers who could resign to be brought to party organisation in preparation for the elections."
	concepts = get_Text_Concepts(text)
	categories = get_Text_Categories(text)
	yahooapires = get_Content_Analysis(text)
	calaisapires = get_Calais_Topics(text)



