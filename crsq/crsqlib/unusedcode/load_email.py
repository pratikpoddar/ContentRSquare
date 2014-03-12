import pickle
from bs4 import BeautifulSoup
from crsq.crsqlib.text_summarize import text_summarize
from crsq.crsqlib import doc_sim

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

#file=open('pratikgmaildumpextended.txt','r')
#emails = pickle.load(file)
#file.close()
#documents = map(lambda x: removeNonAscii(x['ShortBody']), emails)

def closest_related_email(documents, emails, inputnum, algo):

	sim = None
	if algo=="tfidf":
		sim = create_tfidf(documents)
		sim = sim[inputnum]
	if algo=="lsi":
		sim = create_lsi(documents, emails[inputnum]['ShortBody'])

	if sim==None:
		return

	print str(inputnum) + " " + removeNonAscii(emails[inputnum]['Subject']) 
        l = sorted(enumerate(sim),key=lambda x: -x[1])[1:]
	top5emails = []
        for elem in l:
        	if emails[elem[0]]['Subject'].lower().replace('re: ','') != emails[inputnum]['Subject'].lower().replace('re: ',''):
                	print str(elem[0]) + " " + removeNonAscii(emails[elem[0]]['Subject'])
	                top5emails.append(elem[0])
			if len(top5emails)>=5:
				return top5emails

	return top5emails

def closest_links(emails, inputnum):
	return map(lambda x: x['url'], ArticleTags.objects.filter(tag__in=map(lambda x: slugify(x), emails[inputnum]['Tags'])).values('url'))

#links = sum(map(lambda x: x['Links'], emails), [])

