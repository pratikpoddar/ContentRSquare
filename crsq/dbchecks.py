from crsq.models import *

l1 = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
l2 = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))
print "Links in TweetLinks but not in ArticleInfo"
print set(l2)-set(l1)



