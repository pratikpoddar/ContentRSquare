from crsq.models import *
from functools32 import lru_cache

# For Article Group - welcome.html
@lru_cache(maxsize=1024)
def getRelevantTagDict():

        #relevanttags = list(set(map(lambda x: x['tag'], ImportantTags.objects.filter(source="nltk_ne_tag").values('tag')) + map(lambda x: x['tag'], ImportantTags.objects.filter(source__startswith="google_trend").values('tag')) + map(lambda x: x['tag'], ImportantTags.objects.filter(source="top_tag").order_by('-time').values('tag')[:1000])))

        relevanttags = list(set(map(lambda x: x['tag'], ImportantTags.objects.filter(source__startswith="google_trend").values('tag')) + map(lambda x: x['tag'], ImportantTags.objects.filter(source="top_tag").order_by('-time').values('tag')[:2000])))

        relevanttags = sorted(list(set(relevanttags)))
        alphabets = sorted(list(set(map(lambda x:x[0], relevanttags))))
        tagdict = {}
        for alphabet in alphabets:
                tagdict[alphabet] = filter(lambda x: x[0]==alphabet, relevanttags)

	return tagdict

# For ArticleGroup - welcome.html, tagpage.html
@lru_cache(maxsize=1024)
def getRelevantTags():

        relevanttags = list(set(map(lambda x: x['tag'], ImportantTags.objects.filter(source__startswith="google_trend").values('tag')) + map(lambda x: x['tag'], ImportantTags.objects.filter(source="top_tag").order_by('-time').values('tag')[:2000])))

        relevanttags = sorted(list(set(relevanttags)))

	return relevanttags





