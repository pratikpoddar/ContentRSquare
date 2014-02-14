from crsq.models import *
from crsq.crsqlib import urlutils
from urlparse import urlparse
import pickle
from django.db.models import Count

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
print "Average Number of Tags for a Link"
print len(l4) / len(set(l4))
print "Links in ArticleInfo that are not articles"
l5 = filter(lambda x: not urlutils.is_url_an_article(x), list(set(l1)))
print l5
print "Links in TweetLinks that are not articles"
l6 = filter(lambda x: not urlutils.is_url_an_article(x), list(set(l2)))
print l6
#print "Links in ArticleInfo that are short links"
#l7 = filter(lambda x: urlutils.isShortUrlPossibly(x), list(set(l1)))
#print l7
print "Links in TweetLinks that are short links"
l8 = filter(lambda x: urlutils.isShortUrlPossibly(x), list(set(l2)))
print l8
#print "Links in ArticleInfo that do not have date"
#l9 = map(lambda x: x['url'], ArticleInfo.objects.filter(articledate=None).values('url'))
#print l9
#print "All Domains in TweetLinks"
#l10 = list(set(map(lambda x: urlparse(x)[1], l2)))
#print l10
toptags = map(lambda x: x['tag'], ArticleTags.objects.values('tag').annotate(Count('url')).order_by('-url__count')[:1000])
toptags = filter(lambda x: x not in ['something', 'users', 'official', 'process', 'building', 'default', 'profile', 'associated', 'login'], toptags)
tagfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/toptags.txt', 'w')
pickle.dump(toptags, tagfile)
tagfile.close()



