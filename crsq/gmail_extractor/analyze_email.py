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
from random import shuffle
import email
import json
from crsq.crsqlib.emailutils.emailutils import emailstr2tuples

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
	output = []
        try:
            if (tree.pos()[0][1] == 'IN') and (tree.pos()[0][0] in ['in', 'at', 'on']):
		output.append(tree[1])
                for child in tree[1]:
                    output.append(child)
            for child in tree:
                output += get_possible_event_tags(child)
        except:
            pass
	
	return output

def is_introduction_email(emailfrom, emailto, emailcc, emailbcc, body, emailtime):

        emailvec = filter(lambda x: x, [emailfrom, emailto, emailcc, emailbcc])
	emailstring = ', '.join(emailvec)

	emailtuples = emailstr2tuples(emailstring)
	
	emaillist = map(lambda x: x[1].lower(), emailtuples)

	print emaillist

	possibleintro = []

	for e in emaillist:
		previousemails = filter(lambda x: e in ' '.join(filter(lambda t: t, [x['emailfrom'], x['emailto'], x['emailccto'], x['emailbccto']])) > 0, EmailInfo.objects.filter(emailtime__lt=emailtime).values())

		if len(previousemails)<2:
			possibleintro.append(e.strip())

	intro_words = ['connect', 'welcome', 'connect', 'meet', 'introduce', 'introduction', 'introducing', 'invite', 'join', 'appoint', 'pleasure to', 'happy to', 'glad to']
	
	if len(possibleintro) == 0:
		return ''
	if len(filter(lambda x: body.lower().find(x)>=0, intro_words)) == 0:
		return ''

	output = []
	for pi in possibleintro:
		y = filter(lambda x: x[1]==pi, emailtuples)[0]
		if body.lower().find(y[0].split(' ')[0].lower())>0:
			output.append(y[0] + "<" + y[1] + ">")


	return ', '.join(output)

def analyze_body(body):

	cleanbody = removeNonAscii(getBStext(body).strip())
	links = filter(lambda y: (y.find("http:")>=0) or (y.find("https:")>=0),  map(lambda x: x['href'], BeautifulSoup(body).find_all('a', {'href': True})))

	parsed_cleanbody = EFZP.parse(cleanbody)
	efzpshortbody = parsed_cleanbody['body']
	efzpsignature = parsed_cleanbody['signature']

	#shortbody = removeNonAscii(' '.join(map(lambda x: getBStext(x.content),  filter(lambda y: not y.quoted, email_reply_parser.EmailReplyParser.read(body).fragments)))).strip()
	shortbody = ''
		
	tags = list(set(map(lambda x: slugify(x), text_summarize.get_text_tags(cleanbody))))
	tags = map(lambda x: x.replace('-',' '), tags)
	tags = sorted(tags, key=lambda x: article_elastic_search.num_articles_search_exact(x))
	tags = removeNonAscii(' '.join(tags))

	#eventtags = str(event_tags)
	eventtags = ''

	event_tags_ner = text_summarize.get_nltk_ne_ner(cleanbody)
	eventtags2 = json.dumps(event_tags_ner)

	#places = geodict_lib.find_locations_in_text(cleanbody)

	return { 'cleanbody': cleanbody, 'links': links, 'shortbody': shortbody, 'efzpshortbody': efzpshortbody, 'efzpsignature': efzpsignature, 'eventtags2': eventtags2, 'tags': tags, 'eventtags': eventtags }

def analyze_emails(emailhashes):
	print len(emailhashes)
	for eh in emailhashes:
		print eh
		e = EmailInfo.objects.filter(emailhash=eh).values()[0]
		if e['emailfrom'].find('.')>-1:
			body = e['body']
			d = analyze_body(body)
			intro_email = is_introduction_email(e['emailfrom'], e['emailto'], e['emailccto'], e['emailbccto'], e['cleanbody'], e['emailtime'])
			print "...analyzed"
			ei = EmailInfo.objects.get(emailhash=eh)
			ei.shortbody = d['shortbody']
			ei.cleanbody = d['cleanbody']
			ei.efzpshortbody = d['efzpshortbody']
			ei.efzpsignature = d['efzpsignature']
			ei.tags = d['tags']
			ei.eventtags = d['eventtags']
			ei.eventtags2 = d['eventtags2']
			ei.introductiontags = str(intro_email)
			try:
				ei.save()
			except Exception as exc:
				print exc
			for l in d['links']:
				if EmailLinks.objects.filter(emailhash=eh, link=l).count()==0:
					try:
						el = EmailLinks(emailhash=eh, link=l)
						el.save()
					except Exception as exc:
						print exc

emailhashes = map(lambda x: x['emailhash'], EmailInfo.objects.filter(cleanbody='').values('emailhash'))
#emailhashes = map(lambda x: x['emailhash'], EmailInfo.objects.all().values('emailhash'))
analyze_emails(emailhashes)

