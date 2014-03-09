import pickle
from crsq.crsqlib.emailutils import EFZP
from bs4 import BeautifulSoup
from crsq.crsqlib.text_summarize import text_summarize
from sklearn.feature_extraction.text import TfidfVectorizer

def index_of_max(l):
	return sorted(enumerate(l),key=lambda x: x[1])[-2][0]

file=open('pratikgmaildump.txt','r')
emails1 = pickle.load(file)
file.close()
emails1 = emails1[:100]
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
counter=0
for email in emails2:
	print "Analyzing " + str(counter) + "/" + str(len(emails2))
	counter+=1
	extra_info = analyze_body(email['Body'])
	emails3.append(dict(email.items() + extra_info.items()))

file=open('pratikgmaildumpextended.txt','w')
pickle.dump(emails3, file)
file.close()


