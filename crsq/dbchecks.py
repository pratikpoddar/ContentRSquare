from crsq.models import *
from crsq.crsqlib import urlutils
from crsq.crsqlib.text_summarize import text_summarize
from urlparse import urlparse
import pickle
from django.db.models import Count

l1 = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
l2 = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))
l3 = map(lambda x: x['url'], ArticleSemantics.objects.all().values('url'))
l4 = map(lambda x: x['url'], ArticleTags.objects.all().values('url'))
print "Links in TweetLinks but not in ArticleInfo set(l2)-set(l1)"
print set(l2)-set(l1)
print "Links in ArticleInfo but not in ArticleSemantics set(l1)-set(l3)"
print set(l1)-set(l3)
#print "Links in ArticleInfo but not in ArticleTags set(l1)-set(l4)"
#print set(l1)-set(l4)
print "Links in ArticleSemantics but not in ArticleInfo set(l3)-set(l1)"
print set(l3)-set(l1)
print "Links in ArticleTags but not in ArticleInfo set(l4)-set(l1)"
print set(l4)-set(l1)
print "Average Number of Tags for a Link"
print len(l4) / len(set(l4))
print "Links in ArticleInfo that are not articles l5"
l5 = filter(lambda x: not urlutils.is_url_an_article(x), list(set(l1)))
print l5
print "Links in TweetLinks that are not articles l6"
l6 = filter(lambda x: not urlutils.is_url_an_article(x), list(set(l2)))
print l6
print "Links in ArticleInfo that are short links l7"
l7 = filter(lambda x: len(x)<30, filter(lambda x: urlutils.isShortUrlPossibly(x), list(set(l1))))
print l7
print "Links in TweetLinks that are short links l8"
l8 = filter(lambda x: len(x)<30, filter(lambda x: urlutils.isShortUrlPossibly(x), list(set(l2))))
print l8
#print "Links in ArticleInfo that do not have date"
#l9 = map(lambda x: x['url'], ArticleInfo.objects.filter(articledate=None).values('url'))
#print l9
#print "All Domains in TweetLinks"
#l10 = list(set(map(lambda x: urlparse(x)[1], l2)))
#print l10
print "Duplicate urls tobedeleted"
co = map(lambda x: x['articlecontent'], ArticleInfo.objects.all().values('articlecontent'))
import collections
dup_co = [x for x, y in collections.Counter(co).items() if y > 1]
urlgroups = map(lambda co: map(lambda x: x['url'], ArticleInfo.objects.filter(articlecontent=co).values('url')), dup_co)
tobedeleted=[]
for urlgroup in urlgroups:
    for url1 in urlgroup:
        for url2 in urlgroup:
            if (url1.find(url2)>=0) and (len(url1)>len(url2)):
		tobedeleted.append(url1)
print tobedeleted
l11 = map(lambda x: x['url'], ArticleInfo.objects.filter(url__contains="/~r/").values('url'))
l12 = map(lambda x: x['url'], ArticleInfo.objects.filter(url__contains="http://feed").values('url'))
print "ArticleInfo Links which are almost surely there by mistake l11+l12"
print l11+l12
l13 = map(lambda x: x['url'], filter(lambda x: len(x['articlecontent'])<250, ArticleInfo.objects.all().values('articlecontent','url')))
print "Too short Articles l13"
print l13


