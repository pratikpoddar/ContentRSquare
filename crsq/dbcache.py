from crsq.models import *
from functools32 import lru_cache

@lru_cache(maxsize=1024)
def getRelevantTags():

        relevanttags = sorted(filter(lambda x: len(x)<20, list(set(map(lambda x: x['tag'], ImportantTags.objects.all().values('tag'))))))

	return relevanttags


