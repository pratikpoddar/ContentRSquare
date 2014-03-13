import pickle
from crsq.crsqlib.emailutils import EFZP, email_reply_parser
from bs4 import BeautifulSoup
from crsq.crsqlib.text_summarize import text_summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from crsq.models import EmailInfo, EmailLinks

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def analyze_body(body):
	cleanbody = BeautifulSoup(body).text.strip().replace('\r',' ').replace('\n', ' ').strip()
	links = filter(lambda y: (y.find("http:")>=0) or (y.find("https:")>=0),  map(lambda x: x['href'], BeautifulSoup(body).find_all('a', {'href': True})))
	#parsed_cleanbody = EFZP.parse(cleanbody)
	shortbody = removeNonAscii(' '.join(map(lambda x: removeNonAscii(BeautifulSoup(removeNonAscii(x.content)).text).decode('quopri'),  filter(lambda y: not y.quoted, email_reply_parser.EmailReplyParser.read(body).fragments)))).replace('\r', ' ').replace('\n', ' ').strip()
	return { 'cleanbody': cleanbody, 'links': links, 'shortbody': shortbody }

messageids = map(lambda x: x['messageid'], EmailInfo.objects.filter(cleanbody='').values('messageid'))
print len(messageids)
for mid in messageids:
	print mid
	body = EmailInfo.objects.filter(messageid=mid).values('body')[0]['body']
	d = analyze_body(body)
	print "...analyzed"
	ei = EmailInfo.objects.get(messageid=mid)
	ei.shortbody = d['shortbody']
	ei.cleanbody = d['cleanbody']
	try:
		ei.save()
	except Exception as exc:
		print exc
	for l in d['links']:
		if EmailLinks.objects.filter(messageid=mid, link=l).count()==0:
			try:
				el = EmailLinks(messageid=mid, link=l)
				el.save()
			except Exception as exc:
				print exc


