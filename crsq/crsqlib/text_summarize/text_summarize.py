#!/usr/bin/python
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
from topia.termextract import extract
from functools32 import lru_cache
import inspect

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from pyteaser import Summarize

from crsq import crsqlib
from crsq.models import *

from crsq.crsqlib.text_summarize import text_topic_brown

from django.template.defaultfilters import slugify

import logging

logger = logging.getLogger(__name__)

alchemyapi = AlchemyAPI()
calais = Calais("rjfq8eq99bwum4fp3ncjafdw", submitter="python-calais-content-r-square")

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def crsq_unicode(s):

        if s  == None:
                return s

        if isinstance(s, unicode):
                return s
        else:
                return s.decode('utf-8')

def get_text_tags(text):

	output_tags = []
	text = crsq_unicode(text)

	try:
		output_tags += get_nltk_ne(text, tag_meaning=False)
	except Exception as e:
		logger.exception('text_summarize.py - get_text_tags - error - ' + str(e))
		pass

	try:
		if output_tags:
			## adding to the list of nltk ne tags
			for tag in list(set(map(lambda x: slugify(x), output_tags))):
				if ImportantTags.objects.filter(tag=tag, source="nltk_ne_tag").count()==0:
					imptag = ImportantTags(tag=tag, source="nltk_ne_tag")
					imptag.save()	
	except Exception as e:
		logger.exception('text_summarize.py - get_text_tags - adding to nltk_ne_tags - error - ' + str(e))
		pass
	
	try:
		output_tags += get_python_tagger(text, tag_meaning=False)
	except Exception as e:
		logger.exception('text_summarize.py - get_text_tags - error - ' + str(e))
		pass

	try:
		output_tags += get_topia_termextract(text, tag_meaning=False)
	except Exception as e:
		logger.exception('text_summarize.py - get_text_tags - error - ' + str(e))
		pass

	return list(set(output_tags))

def get_text_summary(text, title = None, library="sumy"):

	text = crsq_unicode(text)
	if library == "sumy":
		try:
			summary = ""
			LANGUAGE = "english"

			parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
			stemmer = Stemmer(LANGUAGE)
			summarizer = Summarizer(stemmer)
			summarizer.stop_words = get_stop_words(LANGUAGE)

	    		for sentence in summarizer(parser.document, 4):
        			summary += sentence._text + " "

			return summary.strip()
		except Exception as e:
			logger.exception('text_summarize.py - get_text_summary - error - ' + str(e))
			raise	

	if library == "pyteaser":
		try:
			return ' '.join(Summarize(title, text)[0:4]).strip()
		except Exception as e:
			logger.exception('text_summarize.py - get_text_summary - error - ' + str(e))
			raise

def get_text_topic(text):

	text = crsq_unicode(text)
	try:	
		return crsq_unicode(text_topic_brown.get_text_topic(text))
	except Exception as e:
		logger.exception('text_summarize.py - get_text_topic - error - ' + str(e))
		raise

def get_python_tagger(text, tag_meaning=True):

	text = crsq_unicode(text)
        logger.debug('## Python Tagger ##')
	weights = pickle.load(open(inspect.getfile(tagger)[0:-10]+"data/dict.pkl", 'rb')) 
	myreader = tagger.Reader()
	mystemmer = tagger.Stemmer()
	myrater = tagger.Rater(weights)
	mytagger = tagger.Tagger(myreader, mystemmer, myrater)
	tags = list(mytagger(text, 5))

	tags = map(lambda x: x.string, tags)
	tags = filter(lambda x: x.replace(' ','').isalnum(), tags)
	tags = filter(lambda x: not unicode(x).replace(' ','').isdecimal(), tags)
	logger.debug(tags)
	
	if tag_meaning:

		responseOutput = []
	        for tag in tags:
			try:
	        	        responseOutput.append({'text': tag, 'freebase': get_Freebase_Meaning(tag), 'source': "get_python_tagger"})
			except Exception as e:
				logger.exception('text_summarize.py - get_python_tagger - error - ' + str(e))
				raise

	        responseOutput = filter(lambda x: x['freebase'] != None, responseOutput)
	        try:
        	        logger.debug(responseOutput)
        	except:
                	pass
	        return responseOutput
	else:
		return tags
	

def get_nltk_ne(text, tag_meaning=True):

	text = crsq_unicode(text)
	logger.debug('## NLTK NE ##')
	try:
	        pos_tags = nltk.pos_tag(nltk.word_tokenize(text))
	        ne = nltk.ne_chunk(pos_tags, binary=True)
	        tags = []
        	for i in range(len(ne)):
	                try:
	                        if (ne[i].node=="NE"):
        	                        tags.append(' '.join(map(lambda x: x[0], ne[i].leaves())))
	                except:
        	                pass

	        tags = filter(lambda x: len(x)>4, tags)
		tags = filter(lambda x: x.replace(' ','').isalnum(), tags)
		tags = filter(lambda x: not unicode(x).replace(' ','').isdecimal(), tags)
		logger.debug(tags)

		if tag_meaning:
			responseOutput = []
		        for ne in tags:
		                responseOutput.append({'text': ne, 'freebase': get_Freebase_Meaning(ne), 'source': "get_nltk_ne"})

        		responseOutput = filter(lambda x: x['freebase'] != None, responseOutput)
			logger.debug(responseOutput)
			return responseOutput
		else:
			return tags

	except Exception as e:
		logger.exception('text_summarize.py - get_nltk_ne - error - '+ str(e))
		raise

def get_topia_termextract(text, tag_meaning=True):

	text = crsq_unicode(text)
        logger.debug('## Topia Termextract ##')
	try:
		extractor = extract.TermExtractor()
		tags = extractor(text)
		tags = map(lambda x: x[0], filter(lambda x: len(x[0])>6, tags))
		tags = filter(lambda x: x.replace(' ','').isalnum(), tags)
		tags = filter(lambda x: not unicode(x).replace(' ','').isdecimal(), tags)
		logger.debug(tags)

		if tag_meaning:
			responseOutput = []
	
			for tag in tags:
				responseOutput.append({'text': str(tag), 'freebase': get_Freebase_Meaning(str(tag)), 'source': "get_topia_termextract"})

			responseOutput = filter(lambda x: x['freebase'] != None, responseOutput)
        	        logger.debug(responseOutput)
		else:
			return tags
	
	except Exception as e:
                logger.exception('text_summarize.py - get_topia_termextract - error - '+ str(e))
		raise

        return responseOutput


def get_Text_Concepts(text):

	text = crsq_unicode(text)
	response = alchemyapi.concepts('text', text)

	if response['status'] == 'OK':
		logger.debug('## Alchemy Concepts ##')
		responseOutput = []
		for concept in response['concepts']:
			logger.debug(removeNonAscii('text: ' + concept['text'] + ' ' + concept['relevance']))
			responseOutput.append({'text': concept['text'], 'freebase': get_Freebase_Meaning(concept['text']), 'source': "get_Text_Concepts"})
		return responseOutput
	else:
		logger.exception('text_summarize.py - get_Text_Concepts - error - '+ response['statusInfo'])
		raise

def get_Text_Categories(text):

	text = crsq_unicode(text)
	response = alchemyapi.category('text',text)

	if response['status'] == 'OK':
		logger.debug('## Alchemy Category ##')
		responseOutput = {}
		logger.debug(removeNonAscii('text: '+ response['category'] + ' ' + response['score']))
		if response['category'] == "unknown":
			responseOutput = None
		else:
			responseOutput = {'text': response['category'], 'freebase': get_Freebase_Meaning(response['category']), 'source': "get_Text_Categories" }
		return responseOutput
	else:
                logger.exception('text_summarize.py - get_Text_Categories - error - '+ response['statusInfo'])
		raise

def get_Content_Analysis(text):
	
	text = crsq_unicode(text)
	url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20contentanalysis.analyze%20where%20text%3D%22" + urllib.quote_plus(re.compile('\W+').sub(' ', text).strip()) + "%22&diagnostics=true"

	try:
		root = etree.fromstring(urllib2.urlopen(url).read())
		relevantlist = root.getchildren()[1].getchildren()
	        logger.debug('## Yahoo Content Analysis ##')
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
		logger.debug(responseOutput)
		return responseOutput
	except Exception as e:
                logger.exception('text_summarize.py - get_Content_Analysis - error - '+ str(e))
		raise
		

def get_Calais_Topics(text):
	
	text = crsq_unicode(text)
	calais_result = calais.analyze(text)
	logger.debug('## Open Calais ##')
	responseOutput = []
	try:
		logger.debug("Calais Topics")
		responseOutput += map(lambda x: {'text': x['name'], 'source': 'calais_topics', 'freebase': get_Freebase_Meaning(x['name'])}, calais_result.topics)
		logger.debug(responseOutput)
	except Exception as e:
                logger.exception('text_summarize.py - get_Calais_Topics - error - '+ str(e))
		raise

	try:
		logger.debug("Calais Entities")
		responseOutput += map(lambda x: {'text': x['name'], 'source': 'calais_entities', 'freebase': get_Freebase_Meaning(x['name'])}, calais_result.entities)
		logger.debug(responseOutput)
	except Exception as e:
                logger.exception('text_summarize.py - get_Calais_Topics - error - '+ str(e))
		raise
	
	#responseOutput = filter(lambda x: x['freebase'] != None, responseOutput)
	try:
		logger.debug(responseOutput)
	except:
		pass

	return responseOutput

@lru_cache(maxsize=4096)
def get_Freebase_Meaning(term):

	try:
		term = crsq_unicode(term)
		url = "https://www.googleapis.com/freebase/v1/search?key=AIzaSyCIeO8t4Su2hM0hm8t3aGCgiApBLu7MvGE&query=" + urllib.quote_plus(term)
		jsonResult = json.loads(urllib2.urlopen(url).read())['result']
		if jsonResult:
			if jsonResult[0]['score']>100:
				try:
					return {'parentnode': jsonResult[0]['notable']['name'], 'wikilink': jsonResult[0]['id'], 'title': jsonResult[0]['name']}
				except:
					try:
						return {'parentnode': '', 'wikilink': jsonResult[0]['id'], 'title': jsonResult[0]['name']}
					except:
						try:
							return {'parentnode': jsonResult[0]['notable']['name'], 'wikilink': '', 'title': ''}
						except:
							return None
			else:
				return None
		else:
			return None
	except Exception as e:
                logger.exception('text_summarize.py - get_Freebase_Meaning - error - '+ str(e))
		return None

if __name__=="__main__":	
	text = "In a shake up ahead of the LS polls, environment minister Jayanthi Natarajan resigned from the Union council of ministers. More resignations may be in line for being drafted into party work. The resignation of 59-year-old Natarajan, minister of state with independent charge of environment and forests, has been accepted by the President, a Rashtrapati Bhavan communique said. It also said that oil minister M Veerappa Moily will hold additional charge of the environment ministry. Natarajan, a senior member of Rajya Sabha doing a third term, hails from Tamil Nadu and was brought into the ministry two years ago. Sources said Natarajan, who has, of late, been more visible on television channels defending the party, may be drafted for organisation work. Sources said there could be some more ministers who could resign to be brought to party organisation in preparation for the elections."
	concepts = get_Text_Concepts(text)
	categories = get_Text_Categories(text)
	yahooapires = get_Content_Analysis(text)
	calaisapires = get_Calais_Topics(text)
	topiatermextract = get_topia_termextract(text)
	nltkne = get_nltk_ne(text)
	pythontagger = get_python_tagger(text)




