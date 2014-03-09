import pickle
from bs4 import BeautifulSoup
from crsq.crsqlib.text_summarize import text_summarize
from sklearn.feature_extraction.text import TfidfVectorizer

file=open('pratikgmaildumpextended.txt','r')
emails = pickle.load(file)
file.close()

tfidf = TfidfVectorizer().fit_transform(map(lambda x: x['CleanBody'], emails))
sim = (tfidf * tfidf.T).A

def closest_related_email(inputnum, emails):
	print emails[inputnum]['Subject']
	l = sim[inputnum]
	l2 = sorted(enumerate(l),key=lambda x: -x[1])[1:]
	for elem in l2:
		if emails[elem[0]]['Subject'].lower().replace('re: ','') != emails[inputnum]['Subject'].lower().replace('re: ',''):
			print emails[elem[0]]['Subject']
			return elem[0]			
	

