from crsq.models import *
from crsq.crsqlib import urlutils
from crsq.crsqlib.text_summarize import text_summarize
from urlparse import urlparse
import pickle
from django.db.models import Count

toptagshelp = map(lambda x: x['tag'], ArticleTags.objects.values('tag').annotate(Count('url')).order_by('-url__count')[:500])
toptags = []
for t in toptagshelp:
	fm = text_summarize.get_Freebase_Meaning(t.replace('-',' '))
	try:
		if fm['wikilink']:
			toptags.append(t)
	except:
		pass
toptags = list(set(toptags))
tagfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/toptags.txt', 'w')
pickle.dump(toptags, tagfile)
tagfile.close()

alltags = list(set(map(lambda x: x['tag'], ArticleTags.objects.values('tag'))))
top3000tags = list(set(map(lambda x: x['tag'], ArticleTags.objects.values('tag').annotate(Count('url')).order_by('-url__count')[:1500])))

tagfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/toptags.txt', 'r')
toptags = pickle.load(tagfile)
tagfile.close()

tagfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/nltk_ne_tags.txt', 'r')
nltk_ne_tags = pickle.load(tagfile)
tagfile.close()

from crsq.google_trends.gt import *
google_trends = get_all_google_trends()
google_trends = {k: list(set(filter(lambda x: x in alltags, v))) for k, v in google_trends.items()}
tagfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/googletrendstags.txt', 'w')
pickle.dump(google_trends, tagfile)
tagfile.close()

google_trends_tags = list(set(sum(google_trends.values(), [])))
nltk_ne_tags = filter(lambda x: x in top3000tags, nltk_ne_tags)

relevant_tags = list(set(nltk_ne_tags + google_trends_tags))
tagfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/relevanttags.txt', 'w')
pickle.dump(relevant_tags, tagfile)
tagfile.close()


