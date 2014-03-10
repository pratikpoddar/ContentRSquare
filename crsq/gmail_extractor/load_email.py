import pickle
from bs4 import BeautifulSoup
from crsq.crsqlib.text_summarize import text_summarize

execfile("doc_sim.py")
from sklearn.feature_extraction.text import TfidfVectorizer

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

file=open('pratikgmaildumpextended.txt','r')
emails = pickle.load(file)
file.close()

documents = map(lambda x: removeNonAscii(x['ShortBody']), emails)

def closest_related_email(documents, emails, inputnum, algo):

	if algo=="tdidf":

		sim = create_tfidf(documents)

		print removeNonAscii(emails[inputnum]['Subject'])
		l = sim[inputnum]
		l2 = sorted(enumerate(l),key=lambda x: -x[1])[1:]
		for elem in l2:
			if emails[elem[0]]['Subject'].lower().replace('re: ','') != emails[inputnum]['Subject'].lower().replace('re: ',''):
				print removeNonAscii(emails[elem[0]]['Subject'])
				return elem[0]

emails[0]['Tags']
links = sum(map(lambda x: x['Links'], emails), [])

