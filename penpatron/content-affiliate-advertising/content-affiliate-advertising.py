from crsqlib.text_summarize import text_summarize
from crsqlib import productsearch
from lxml import objectify
import bottlenose
import hashlib
import pickledb

import logging

logging.basicConfig(filename='logger.log',level=logging.DEBUG, format='[ %(levelname)s ] [ %(asctime)s ] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

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
			return output

		else:
			logging.info('content_affiliate_returns ' + str(db.get(combined_hash)))
			return db.get(combined_hash)
	
	except Exception as e:
		logging.exception('content_affiliate_error ' + str(e))
		output = get_Content_Affliate_Advertising(content, index)
		logging.info('content_affiliate_returns ' + str(output))
		return output

def get_Content_Affliate_Advertising(content, index):

	keywords = []
	#try:
	#	keywords += map(lambda x: x['text'], text_summarize.get_Calais_Topics(content))
	#except:
	#	pass
	
        #try:
        #        keywords += map(lambda x: x['text'], text_summarize.get_Content_Analysis(content))
        #except:
        #        pass

        #try:
        #        keywords += map(lambda x: x['text'], text_summarize.get_Text_Concepts(content))
        #except:
        #        pass

        try:
                keywords += map(lambda x: x['text'], text_summarize.get_nltk_ne(content))
        except:
                pass

        try:
                keywords += map(lambda x: x['text'], text_summarize.get_python_tagger(content))
        except:
                pass

        try:
                keywords += map(lambda x: x['text'], text_summarize.get_topia_termextract(content))
        except:
                pass

	keywords = list(set(keywords))
	#keywords = ["Columbia Business School", "IBM"]

	products = productsearch.getAmazonProducts(keywords, index)
	return products

text = "Disclaimer: It is a made up problem. Not to be attempted by light hearted. Problem: I have a 300 word text. I have a large list of indexed strings (Length of string ~ 20, Number of strings ~ 1M). I need to figure out phrases in the 300 word text that match exactly to one of the strings in the large list of strings I have. A naive approach: Taking all 45000 (300 C 2) phrases, search in the large list of strings. Can we do better than this? We need to minimize calls to list of indexed strings! Problem 1: Consider the problem of picking K elements randomly from N elements. Suggest an algorithm. What is the time and space complexity of your algorithm? Problem 2: Now consider that the stream is infinitely long (i.e. N is unknown). Now how do we pick K elements randomly. Source: IBM Ponder This Dec 12 ( http://domino.research.ibm.com/comm/wwwr_ponder.nsf/challenges/December2012.html ) - Mailed to me by Aashay Harlalka (Final Year Student, CSE, IITB)Problem:36 people live in a 6x6 grid, and each one of them lives in a separate square of the grid. Each resident's neighbors are those who live in the squares that have a common edge with that resident's square.Each resident of the grid is assigned a natural number N, such that if a person receives some N>1, then he or she must also have neighbors that have been assigned all of the numbers 1,2,...,N-1.Find a configuration of the 36 neighbors where the sum of their numbers is at least 90.As an example, the highest sum we can get in a 3x3 grid is 20:1 2 14 3 42 1 2 Source: Mailed to me by Vashist Avadhanula (PhD Student at Columbia Business School, EE IITB 2013 Alumnus)Problem:Consider a case where you flip two fair coins at once (sample space is HH, HT, TH & TT) you repeat this experiment many times and note down the outputs as a sequence. What is the expected number of flips (one flip includes tossing of two coins) to arrive at the sequence HHTHHTT. Source: Mailed to me by Sudeep Kamath (PhD Student, UC at Berkeley, EE IITB Alumnus 2008)Problem:Tricky Question.Let f be a continuous, real-valued function on reals such thatlimit_{n \rightarrow \infty} f(nx) = 0 for all real x.Show limit_{x\rightarrow \infty} f(x) = 0."

index = "Books"

try:
	text = sys.argv[1]
	index = sys.argv[2]

except:
	pass

output = content_affiliate(text, index)
##print "[{'keyword':'Columbia Business School', 'link':'http://www.cseblog.com'}]"
print output


