import re
import pickle
from crsq.crsqlib.emailutils import EFZP, email_reply_parser
from bs4 import BeautifulSoup
from crsq.crsqlib.text_summarize import text_summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from crsq.models import EmailInfo, EmailLinks
from crsq.crsqlib.geodict import geodict_lib
from django.template.defaultfilters import slugify
from crsq.crsqlib import article_elastic_search
import nltk
from stat_parser import Parser
import nltk.data

import sys
sys.stdout = open("email_analyzer.dat", "w+")

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
parser = Parser()

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
def getBStext(html): 
	html = re.sub(r"<br>", ". ", html, flags=re.IGNORECASE)
	sstr = BeautifulSoup(removeNonAscii(html)).stripped_strings
	return removeNonAscii(removeNonAscii(' '.join(sstr)).replace('\r', ' ').replace('\n', ' ').strip().decode('quopri'))

def get_parsed_trees(text):
	sentences = sent_tokenizer.tokenize(text)
	try:
		return map(lambda sentence: parser.parse(sentence), sentences)
	except:
		return []

def get_possible_event_tags(tree):
        try:
            if (tree.pos()[0][1] == 'IN') and (tree.pos()[0][0] in ['in', 'at', 'on']):
                print tree[1]
                for child in tree[1]:
                    print child
            for child in tree:
                get_possible_event_tags(child)
        except:
            pass

def is_introduction_email(emailfrom, emailto, emailcc, emailbcc, body, emailtime):

	emailvec = filter(lambda x: x, [emailfrom, emailto, emailcc, emailbcc])

        allpreviousemails = filter(lambda x: len(filter(lambda y: y in ' '.join(filter(lambda t: t, [x['emailfrom'], x['emailto'], x['emailccto'], x['emailbccto']])), emailvec)) > 0, EmailInfo.objects.all().values())

	previousemails = filter(lambda z: z['emailtime'] < emailtime, allpreviousemails)
	if len(previousemails)>2:
		return 0

	intro_words = ['connect', 'welcome', 'connect', 'glad to meet', 'meet', 'introduce', 'introduction', 'invite', 'join', 'appoint']
	
	if len(filter(lambda x: body.lower().find(x)>=0, intro_words)) == 0:
		return 0

	return 1

def analyze_body(body):

	cleanbody = removeNonAscii(getBStext(body).strip())
	links = filter(lambda y: (y.find("http:")>=0) or (y.find("https:")>=0),  map(lambda x: x['href'], BeautifulSoup(body).find_all('a', {'href': True})))

	parsed_cleanbody = EFZP.parse(cleanbody)
	efzpshortbody = parsed_cleanbody['body']
	efzpsignature = parsed_cleanbody['signature']

	shortbody = removeNonAscii(' '.join(map(lambda x: getBStext(x.content),  filter(lambda y: not y.quoted, email_reply_parser.EmailReplyParser.read(body).fragments)))).strip()
		
	tags = list(set(map(lambda x: slugify(x), text_summarize.get_text_tags(cleanbody))))
	tags = map(lambda x: x.replace('-',' '), tags)
	tags = sorted(tags, key=lambda x: article_elastic_search.num_articles_search_exact(x))
	tags = removeNonAscii(' '.join(tags))

	event_tags = map(lambda x: get_possible_event_tags(x), get_parsed_trees(cleanbody))
	places = geodict_lib.find_locations_in_text(cleanbody)

	return { 'cleanbody': cleanbody, 'links': links, 'shortbody': shortbody, 'efzpshortbody': efzpshortbody, 'efzpsignature': efzpsignature, 'places': places, 'tags': tags }

messageids = map(lambda x: x['messageid'], EmailInfo.objects.filter(cleanbody='').values('messageid'))
#messageids = map(lambda x: x['messageid'], EmailInfo.objects.all().values('messageid'))
#messageids = messageids[:2]

def init():
	print len(messageids)
	for mid in messageids:
		print mid
		body = EmailInfo.objects.filter(messageid=mid).values('body')[0]['body']
		e = EmailInfo.objects.filter(messageid=mid).values()[0]
		d = analyze_body(body)
		intro_email = is_introduction_email(e['emailfrom'], e['emailto'], e['emailccto'], e['emailbccto'], e['cleanbody'], e['emailtime'])
		if intro_email == 1:
			print "Intro Email: " + mid
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


init()
