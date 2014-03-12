import pickle
from crsq.crsqlib.emailutils import EFZP, email_reply_parser
from bs4 import BeautifulSoup
from crsq.crsqlib.text_summarize import text_summarize
from sklearn.feature_extraction.text import TfidfVectorizer

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

file=open('pratikgmaildump.txt','r')
emails1 = pickle.load(file)
file.close()
emails1 = emails1[:80]
emails2 = filter(lambda x: x['From'].find('root@localhost')==-1, emails1)

def analyze_body(body):
	cleanbody = BeautifulSoup(body).text.strip().replace('\r',' ').replace('\n', ' ').strip()
	links = filter(lambda y: (y.find("http:")>=0) or (y.find("https:")>=0),  map(lambda x: x['href'], BeautifulSoup(body).find_all('a', {'href': True})))
	parsed_cleanbody = EFZP.parse(cleanbody)
	shortbody = ' '.join(map(lambda x: removeNonAscii(BeautifulSoup(removeNonAscii(x.content)).text).decode('quopri'),  filter(lambda y: not y.quoted, email_reply_parser.EmailReplyParser.read(body).fragments)))
	tags = text_summarize.get_text_tags(shortbody)
	return { 'CleanBody': cleanbody, 'Links': links, 'ParsedCleanBody': parsed_cleanbody, 'ShortBody': shortbody, 'Tags': tags }

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

