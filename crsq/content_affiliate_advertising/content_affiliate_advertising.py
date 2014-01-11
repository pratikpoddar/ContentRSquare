from crsq.crsqlib.text_summarize import text_summarize
from crsq.crsqlib import productsearch
from lxml import objectify
import bottlenose
import hashlib
import pickledb
import collections
import sys
import logging

logging.basicConfig(filename='logger.log',level=logging.DEBUG, format='[ %(levelname)s ] [ %(asctime)s ] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def convert(d):
    if isinstance(d, basestring):
        return str(d)
    elif isinstance(d, collections.Mapping):
        return dict(map(convert, d.iteritems()))
    elif isinstance(d, collections.Iterable):
        return type(d)(map(convert, d))
    else:
        return d

def content_affiliate(content, index):

	logging.info('content_affiliate_call ' + content[0:100]) 
	try:
		db = pickledb.load('content-affiliate.db', False)
		combined_hash = str(int(hashlib.md5(content.replace(' ','')+index.replace(' ','')).hexdigest(), 16))
		if db.get(combined_hash) == None:
			output = get_Content_Affliate_Advertising(content, index)
			db.set(combined_hash, output)
			db.dump()
			logging.info('content_affiliate_returns ' + str(output))
			return convert(output)

		else:
			logging.info('content_affiliate_returns ' + str(db.get(combined_hash)))
			return convert(db.get(combined_hash))
	
	except Exception as e:
		logging.exception('content_affiliate_error ' + str(e))
		output = get_Content_Affliate_Advertising(content, index)
		logging.info('content_affiliate_returns ' + str(output))
		return convert(output)

def get_Content_Affliate_Advertising(content, index):

	keywords = []

        try:
                keywords += map(lambda x: x['text'], text_summarize.get_nltk_ne(content))
        except Exception as e:
		logging.exception('content-affiliate-advetising get_Content_Affiliate_Advertising ' + str(e) + ' get_nltk_ne')
                pass

        try:
                keywords += map(lambda x: x['text'], text_summarize.get_python_tagger(content))
        except Exception as e:
		logging.exception('content-affiliate-advetising get_Content_Affiliate_Advertising ' + str(e) + ' get_python_tagger')
                pass

        try:
                keywords += map(lambda x: x['text'], text_summarize.get_topia_termextract(content))
        except Exception as e:
		logging.exception('content-affiliate-advetising get_Content_Affiliate_Advertising ' + str(e) + ' get_topia_termextract')
                pass

	keywords = list(set(keywords))
	#keywords = ["Columbia Business School", "IBM"]

	products = []
	try:
		products = productsearch.getAmazonProducts(keywords, index)
	except Exception as e:
		logging.exception('content-affiliate-advetising get_Content_Affiliate_Advertising ' + str(e) + ' get_Amazon_Products')
	return products

text = "Disclaimer: It is a made up problem. Not to be attempted by light hearted. Problem: I have a 300 word text. I have a large list of indexed strings (Length of string ~ 20, Number of strings ~ 1M). I need to figure out phrases in the 300 word text that match exactly to one of the strings in the large list of strings I have. A naive approach: Taking all 45000 (300 C 2) phrases, search in the large list of strings. Can we do better than this? We need to minimize calls to list of indexed strings! Problem 1: Consider the problem of picking K elements randomly from N elements. Suggest an algorithm. What is the time and space complexity of your algorithm? Problem 2: Now consider that the stream is infinitely long (i.e. N is unknown). Now how do we pick K elements randomly. Source: IBM Ponder This Dec 12 ( http://domino.research.ibm.com/comm/wwwr_ponder.nsf/challenges/December2012.html ) - Mailed to me by Aashay Harlalka (Final Year Student, CSE, IITB)Problem:36 people live in a 6x6 grid, and each one of them lives in a separate square of the grid. Each resident's neighbors are those who live in the squares that have a common edge with that resident's square.Each resident of the grid is assigned a natural number N, such that if a person receives some N>1, then he or she must also have neighbors that have been assigned all of the numbers 1,2,...,N-1.Find a configuration of the 36 neighbors where the sum of their numbers is at least 90.As an example, the highest sum we can get in a 3x3 grid is 20:1 2 14 3 42 1 2 Source: Mailed to me by Vashist Avadhanula (PhD Student at Columbia Business School, EE IITB 2013 Alumnus)Problem:Consider a case where you flip two fair coins at once (sample space is HH, HT, TH & TT) you repeat this experiment many times and note down the outputs as a sequence. What is the expected number of flips (one flip includes tossing of two coins) to arrive at the sequence HHTHHTT. Source: Mailed to me by Sudeep Kamath (PhD Student, UC at Berkeley, EE IITB Alumnus 2008)Problem:Tricky Question.Let f be a continuous, real-valued function on reals such thatlimit_{n \rightarrow \infty} f(nx) = 0 for all real x.Show limit_{x\rightarrow \infty} f(x) = 0."

text = "Back in 2012 Id been to enough tech startup conferences in Europe over the previous few years to work out which ones appeared to be most significant. Europe being the disjointed bunch of countries that it is has too many to mention. That ended up being a post about events in 2013. Now, with 2014 already here, I figured plenty of readers would like an update. So here it is. A huge thanks to Heisenberg Media for helping me put this together. Thanks also to Conferize for their crowd-sourced list of European Tech Events in 2014 which you can find here. That is not our list, its theirs, but its pretty good. We also recommend the listing over at Lanyrd. But, simply being listed below does NOT imply that any of these events are endorsed by or partnered with TechCrunch, other than TechCrunch branded ones of course. This is a purely editorial list, based on our experience in Europe, the list is designed to help the European tech scene grow and get more organised. Simple. Why is it important to do this In the first instance, Europe is a bit of a mess. Every single country seems to have its own major conference on tech startups. And so we need a single overview of whats going on."

index = "Books"

#try:
#	text = sys.argv[1]
#	index = sys.argv[2]

#except Exception as e:
#	logging.exception("content-affiliate-advertising - error in input - " + str(e))
#	pass

#output = content_affiliate(text, index)
##print "[{'keyword':'Columbia Business School', 'link':'http://www.cseblog.com'}]"
#print output


