import pickle
from crsq.crsqlib.emailutils import EFZP, email_reply_parser
from bs4 import BeautifulSoup
from crsq.crsqlib.text_summarize import text_summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from crsq.models import EmailInfo, EmailLinks
from crsq.crsqlib.geodict import geodict_lib
from django.template.defaultfilters import slugify

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def analyze_body(body):
	cleanbody = BeautifulSoup(body).text.strip().replace('\r',' ').replace('\n', ' ').strip()
	links = filter(lambda y: (y.find("http:")>=0) or (y.find("https:")>=0),  map(lambda x: x['href'], BeautifulSoup(body).find_all('a', {'href': True})))

	parsed_cleanbody = EFZP.parse(cleanbody)
	efzpshortbody = parsed_cleanbody['body']
	efzpsignature = parsed_cleanbody['signature']

	shortbody = removeNonAscii(' '.join(map(lambda x: removeNonAscii(BeautifulSoup(removeNonAscii(x.content)).text).decode('quopri'),  filter(lambda y: not y.quoted, email_reply_parser.EmailReplyParser.read(body).fragments)))).replace('\r', ' ').replace('\n', ' ').strip()
	
	tags = removeNonAscii(' '.join(list(set(map(lambda x: slugify(x), text_summarize.get_text_tags(cleanbody)))))).replace('-',' ')

	places = geodict_lib.find_locations_in_text(cleanbody)

	return { 'cleanbody': cleanbody, 'links': links, 'shortbody': shortbody, 'efzpshortbody': efzpshortbody, 'efzpsignature': efzpsignature, 'places': places, 'tags': tags }

messageids = map(lambda x: x['messageid'], EmailInfo.objects.filter(cleanbody='').values('messageid'))
messageids = map(lambda x: x['messageid'], EmailInfo.objects.all().values('messageid'))
print len(messageids)
for mid in messageids:
	print mid
	body = EmailInfo.objects.filter(messageid=mid).values('body')[0]['body']
	d = analyze_body(body)
	print "...analyzed"
	ei = EmailInfo.objects.get(messageid=mid)
	ei.shortbody = d['shortbody']
	ei.cleanbody = d['cleanbody']
	ei.efzpshortbody = d['efzpshortbody']
	ei.efzpsignature = d['efzpsignature']
	ei.places = d['places']
	ei.tags = d['tags']
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


