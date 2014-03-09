import pickle
from crsq.crsqlib import EFZP
from bs4 import BeautifulSoup
from crsq.crsqlib.text_summarize import text_summarize
from sklearn.feature_extraction.text import TfidfVectorizer

def index_of_max(l):
	return sorted(enumerate(l),key=lambda x: x[1])[-2][0]

file=open('pratikgmaildump.txt','r')
emails1 = pickle.load(file)
file.close()
emails2 = filter(lambda x: x['From'].find('root@localhost')==-1, emails1)

def analyze_body(body):
	cleanbody = BeautifulSoup(body).text.strip().replace('\r',' ').replace('\n', ' ').strip()
	links = None
	parsed_cleanbody = None
	links = filter(lambda y: (y.find("http:")>=0) or (y.find("https:")>=0),  map(lambda x: x['href'], BeautifulSoup(emails2[4]['Body']).find_all('a', {'href': True})))
	tags = text_summarize.get_text_tags(cleanbody)
	parsed_cleanbody = EFZP.parse(cleanbody)
	return {'CleanBody': cleanbody, 'Links': links, 'ParsedCleanBody': parsed_cleanbody}

emails3 = []
for email in emails2:
	extra_info = analyze_body(email['Body'])
	emails3.append(dict(email.items() + extra_info.items()))

file=open('pratikgmaildumpextended.txt','w')
pickle.dump(emails3, file)
file.close()

tfidf = TfidfVectorizer().fit_transform(map(lambda x: x['CleanBody'], emails3))
sim = (tfidf * tfidf.T).A

def testing_related_email(inputnum):
	print emails3[inputnum]['Subject']
	print emails3[index_of_max(sim[inputnum])]['Subject']


