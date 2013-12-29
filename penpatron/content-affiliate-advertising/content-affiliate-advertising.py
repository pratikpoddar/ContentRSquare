from text_summarize.text_summarize import *
from lxml import objectify
import bottlenose
import hashlib
import pickledb

def content_affiliate(content, index):

	try:
		db = pickledb.load('content-affiliate.db', False)
		combined_hash = str(int(hashlib.md5(content.replace(' ','')+index.replace(' ','')).hexdigest(), 16))
		if db.get(combined_hash) == None:
			output = get_Content_Affliate_Advertising(content, index)
			db.set(combined_hash, output)
			db.dump()
			return output

		else:
			return db.get(combined_hash)
	
	except:
		output = get_Content_Affliate_Advertising(content, index)
		return output

def get_Content_Affliate_Advertising(content, index):

	keywords = []
	try:
		k1 = get_Calais_Topics(content)
	except:
		k1 = []
	
	#try:
	#	k2 = get_Content_Analysis(content)
	#except:
	#	k2 = []

	try:
		k3 = get_Text_Concepts(content)
	except:
		k3 = []

	try:
		k4 = get_nltk_ne(content)
	except:
		k4 = []

	try:
		keywords += map(lambda x: x['text'], k1)
	except:
		pass

	#try:
	#	keywords += map(lambda x: x['text'], k2)
	#except:
	#	pass

	try:
		keywords += map(lambda x: x['text'], k3)
	except:
		pass

	try:
		keywords += map(lambda x: x['text'], k4)
	except:
		pass

	keywords = list(set(keywords))
	#keywords = ["Columbia Business School", "IBM"]

	secret_key = '1U8FN957RXcYjF+3nRBUSrt7GFo5qOikY7r2sKYC'
	access_key = 'AKIAJN7RCVYN23USSAYQ'
	associate_tag = 'cb02-20'

	amazon = bottlenose.Amazon(access_key, secret_key, associate_tag)
	output = []

	for kw in keywords:
		try:
		        response = amazon.ItemSearch(Title=kw, SearchIndex=index, ResponseGroup="ItemAttributes")
		        root = objectify.fromstring(response)
			if root.Items.Item.ASIN:
		        	link = "http://www.amazon.com/dp/"+("000000"+str(root.Items.Item.ASIN)+"/")[-11:-1]+"?tag=cb02-20"
				output.append({'keyword': kw, 'link': link})
		except Exception as e:
			print e
			pass

	return output		

text = "Disclaimer: It is a made up problem. Not to be attempted by light hearted. Problem: I have a 300 word text. I have a large list of indexed strings (Length of string ~ 20, Number of strings ~ 1M). I need to figure out phrases in the 300 word text that match exactly to one of the strings in the large list of strings I have. A naive approach: Taking all 45000 (300 C 2) phrases, search in the large list of strings. Can we do better than this? We need to minimize calls to list of indexed strings! Problem 1: Consider the problem of picking K elements randomly from N elements. Suggest an algorithm. What is the time and space complexity of your algorithm? Problem 2: Now consider that the stream is infinitely long (i.e. N is unknown). Now how do we pick K elements randomly. Source: IBM Ponder This Dec 12 ( http://domino.research.ibm.com/comm/wwwr_ponder.nsf/challenges/December2012.html ) - Mailed to me by Aashay Harlalka (Final Year Student, CSE, IITB)Problem:36 people live in a 6x6 grid, and each one of them lives in a separate square of the grid. Each resident's neighbors are those who live in the squares that have a common edge with that resident's square.Each resident of the grid is assigned a natural number N, such that if a person receives some N>1, then he or she must also have neighbors that have been assigned all of the numbers 1,2,...,N-1.Find a configuration of the 36 neighbors where the sum of their numbers is at least 90.As an example, the highest sum we can get in a 3x3 grid is 20:1 2 14 3 42 1 2 Source: Mailed to me by Vashist Avadhanula (PhD Student at Columbia Business School, EE IITB 2013 Alumnus)Problem:Consider a case where you flip two fair coins at once (sample space is HH, HT, TH & TT) you repeat this experiment many times and note down the outputs as a sequence. What is the expected number of flips (one flip includes tossing of two coins) to arrive at the sequence HHTHHTT. Source: Mailed to me by Sudeep Kamath (PhD Student, UC at Berkeley, EE IITB Alumnus 2008)Problem:Tricky Question.Let f be a continuous, real-valued function on reals such thatlimit_{n \rightarrow \infty} f(nx) = 0 for all real x.Show limit_{x\rightarrow \infty} f(x) = 0."

index = "Books"

try:
	text = sys.argv[1]
	index = sys.argv[2]
	output = content_affiliate(text, index)
	##print "[{'keyword':'Columbia Business School', 'link':'http://www.cseblog.com'}]"
	print output
except:
	pass


