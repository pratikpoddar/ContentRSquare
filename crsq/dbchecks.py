from crsq.models import *

l1 = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
l2 = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))
l3 = map(lambda x: x['url'], ArticleSemantics.objects.all().values('url'))
l4 = map(lambda x: x['url'], ArticleTags.objects.all().values('url'))
print "Links in TweetLinks but not in ArticleInfo"
print set(l2)-set(l1)
print "Links in ArticleInfo but not in ArticleSemantics"
print set(l1)-set(l3)
print "Links in ArticleInfo but not in ArticleTags"
print set(l1)-set(l4)
print "Links in ArticleSemantics but not in ArticleInfo"
print set(l3)-set(l1)
print "Links in ArticleTags but not in ArticleInfo"
print set(l4)-set(l1)





