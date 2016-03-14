from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from django.templatetags.static import static
from django.db.models import Count

from collections import Counter

from django.core.context_processors import csrf

import re
import urllib
import urllib2
from datetime import date, timedelta, datetime
import pytz
import pickle
import logging
import urlparse
import json
from crsq.content_affiliate_advertising import content_affiliate_advertising
from crsq.twitter_newspaper import twitter_newspaper
from crsq import dbcache
from crsq.models import ArticleInfo, ArticleSemantics, ArticleTags, ImportantTags, EmailInfo, ZnInputTag, ZnTagVisit

from crsq.crsqlib import article_elastic_search, email_elastic_search, text_summarize

from dateutil.parser import parse as dateutilparse

import collections
import pygeoip

import random
from crsq.crsqlib.emailutils.emailutils import emailstr2tuples, relatedemailaddr
import time
from django.conf import settings

from crsq import whatistrending

logger = logging.getLogger(__name__)

# time.sleep(60)  # Delay for 1 minute (60 seconds)

relevanttags = []
#try:
#relevanttags = filter(lambda x: len(x)>4, article_elastic_search.gettopterms())
#except:
relevanttags = filter(lambda x: len(x)>4, dbcache.getRelevantTags())

##########################################################################################
##########################################################################################
##########################################################################################

def loggerdebug(request, string):
	if 'pratik' in request.GET.keys():
		logger.debug(string)
	return

def index(request):
	now = datetime.now()
        html = "<html><body>It is now %s. Please contact Pratik Poddar - pratik 'dot' phodu 'at' gmail 'dot' com - for any query</body></html>" % now
        return HttpResponse(html)

##########################################################################################
##########################################################################################
##########################################################################################

def caa(request):

	if filter(lambda x: x not in request.GET.keys(), ['text','index','jsonp_callback']):
		return HttpResponse("<html><body>Content Affiliate Advertising - Wrong Input</body></html>")

	keywords = content_affiliate_advertising.content_affiliate(request.GET['text'], request.GET['index']) 
	#keywords = [{'keyword':'Columbia Business School', 'link':'http://www.cseblog.com'}]

        jsonresponse = request.GET['jsonp_callback'] + '({"keywords":' + str(keywords) + '})'
	
        return HttpResponse(jsonresponse)

##########################################################################################
##########################################################################################
##########################################################################################

def gmailemailjs(request):

        emailcontent = request.GET['emailcontent']
        tags = text_summarize.text_summarize.get_text_tags(emailcontent)
        tags = ' '.join(tags).strip()
        logger.debug("Gmail Email JS Tags: " + tags)
        if tags == '':
                urls = []
        else:
                urls = article_elastic_search.searchdoc(tags, num=10, threshold=0.4)

        output = ArticleInfo.objects.filter(url__in=urls).values('url', 'articletitle')
        output = json.dumps([dict(x) for x in output])

        jsonresponse = request.GET['jsonp_callback'] + '({"output":' + output + '})'
        return HttpResponse(jsonresponse)

def gmailemailjs_imap(request):

	def getemailaddr(string):
		return filter(lambda x: x.find('@')>0, string.split(' '))[-1].strip()


	def getemailhash(username, fromaddr, subject, dateemail):

		try:
	                logger.debug((username, fromaddr, subject, dateemail))
                        logger.debug(map(lambda x: x['emailhash'], EmailInfo.objects.filter(user__icontains=username, emailfrom__icontains=fromaddr, subject__icontains=subject).values('emailhash')))
                        logger.debug(map(lambda x: x['emailhash'], EmailInfo.objects.filter(user__icontains=username, emailfrom__icontains=fromaddr, subject__icontains=subject, emailtime__range=(dateemail-timedelta(minutes=3),dateemail+timedelta(minutes=2))).values('emailhash')))
			return map(lambda x: x['emailhash'], EmailInfo.objects.filter(user__icontains=username, emailfrom__icontains=fromaddr, subject__icontains=subject, emailtime__range=(dateemail-timedelta(minutes=3),dateemail+timedelta(minutes=2))).values('emailhash'))
		except Exception as exc:
			logger.exception(exc)
			return []

	emailidentifier = request.GET['emailidentifier']
	logger.debug(emailidentifier)
	openthread  = json.loads(emailidentifier)
	username = request.GET['username']
	offset = timedelta(hours=5, minutes=30)

	emailhashes = []
	for openemail in openthread:
                try:
                        dateemail = dateutilparse(openemail['datetime'])-offset
                        dateemail = datetime(dateemail.year, dateemail.month, dateemail.day, dateemail.hour, dateemail.minute, tzinfo=pytz.utc)
                except:
                        dateemail = None
		logger.debug([username, openemail['from_email'], openemail['subject'], dateemail])		
		emailhashes += getemailhash(username, openemail['from_email'], openemail['subject'], dateemail)
		
	emailhashes = filter(lambda x: x, emailhashes)
	rlinks=[]
	for emailhash in emailhashes:
	        e = EmailInfo.objects.filter(emailhash=emailhash).values()[0]
		recommendedlinks = article_elastic_search.searchdoc(e['tags'].replace('-',' ').title(), num=30, threshold=0.25, recencyweight=0.0)
	        recommendedlinks = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=recommendedlinks).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:15])
		rlinks += recommendedlinks[:5]

	output = ArticleInfo.objects.filter(url__in=rlinks).values('url', 'articletitle')
	output = json.dumps([dict(x) for x in output])
	
	jsonresponse = request.GET['jsonp_callback'] + '({"output":' + output + '})'
        return HttpResponse(jsonresponse)

##########################################################################################
##########################################################################################
##########################################################################################

def tw_np(request, sector, location, page=1):

	if (not filter(lambda x: slugify(x)==sector, twitter_newspaper.tw_np_sector_list)) or (not filter(lambda x: slugify(x)==location, twitter_newspaper.tw_np_location_list)):
		return HttpResponse("<html><body>Twitter Newspaper - Wrong Input</body></html>")

	articles = twitter_newspaper.get_articles(sector, location, cursor=int(page)*10-10)[:10]

        article_list = []
        for article in articles:
                article_list.append(dict( article, **{'domain': urlparse.urlparse(article['url'])[1], 'articlesummary' : ArticleSemantics.objects.filter(url=article['url']).values('summary')[0]['summary'], 'sharers': twitter_newspaper.get_sharers(article['url'])}))

	template = loader.get_template('crsq/twitterstreetjournal/index.html')

	context = RequestContext(request, {
	        'article_list': article_list,
		'sector': sector,
		'sectorname': filter(lambda x: slugify(x)==sector, twitter_newspaper.tw_np_sector_list)[0],
		'location': location,
		'locationname': filter(lambda x: slugify(x)==location, twitter_newspaper.tw_np_location_list)[0],
		'sector_list': twitter_newspaper.tw_np_sector_list,
		'location_list': twitter_newspaper.tw_np_location_list,
		'page': int(page),
		'pagerange' : range(max(1,int(page)-2),max(1,int(page)-2)+3)
        })
	return HttpResponse(template.render(context))

def tw_np_redirect(request):
	return redirect('/twitterstreetjournal/technology/san-francisco-usa')

##########################################################################################
##########################################################################################
##########################################################################################

def timenews(request, timeline_news_name):
	
	template = loader.get_template('crsq/timeline-news/timeline.html')
        context = RequestContext(request, {'timeline_name': timeline_news_name})
        return HttpResponse(template.render(context))

def timenews_article(request, articleid):

        article = ArticleInfo.objects.filter(id=int(articleid)).values()[0]
        if not article:
                raise Http404

        domain = urlparse.urlparse(article['url'])[1]
        sharers = twitter_newspaper.get_sharers(article['url'])
        try:
                articlesemantics = ArticleSemantics.objects.filter(url=article['url']).values()[0]
        except:
                articlesemantics = {'summary': None, 'topic': None}

        try:
                articletags = ArticleTags.objects.filter(url=article['url']).values('tag')
                articletags = map(lambda x: x['tag'], articletags)
        except:
                articletags = []

        template = loader.get_template('crsq/timeline-news/article.html')

        context = RequestContext(request, {
                'article' : dict( article, **{'domain': domain, 'sharers': sharers, 'articlesummary' : articlesemantics['summary'], 'topic': articlesemantics['topic'], 'tags': ', '.join(articletags)})
        })
        return HttpResponse(template.render(context))

##########################################################################################
##########################################################################################
##########################################################################################

def getIndexAllowed(tag):
        indexallowed = 0
        if ImportantTags.objects.filter(tag=tag).count()>0:
                indexallowed = 1
		return indexallowed

	if ZnInputTag.objects.filter(tag=tag).count()>0:
        	indexallowed = 1
		return indexallowed

	return indexallowed

def zippednewsapptrending(request, topic, topicname):

	maxid = ArticleInfo.objects.all().order_by("-id")[0].id
	ai = ArticleInfo.objects.filter(id__gt=maxid-500)
	tagname = "top-trending-"+topicname
	tag = tagname
	bi = filter(lambda x: (x['source'].find('feedanalyzerfromscratchhttps://news.google.com/')>=0) and (x['source'].endswith('topic='+topic)), filter(lambda y: y['source'], ai.values('url', 'source')))

	urls = map(lambda x: x['url'], bi)[-40:]
       	random.shuffle(urls)
	if request.mobile:
		urls = urls[:7]
	else:
		urls = urls[:10]
	urls = map(lambda x: x['url'], ArticleSemantics.objects.filter(url__in=urls).exclude(summary=None).exclude(summary='').values('url'))
	urls = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=urls).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url'))
	title = tag.replace('-',' ').title()+ " News - ZippedNews"
	h1title = tag.replace('-',' ').title()+ " News"

        articles = ArticleInfo.objects.filter(url__in=urls).order_by('-id').values()
        articletagsdump = ArticleTags.objects.filter(url__in=urls).values('tag', 'url')
        articletagsdump2 = collections.defaultdict(list)
        articletagslist = list(set(map(lambda x: x['tag'], articletagsdump)))
        for article in articletagsdump:
                articletagsdump2[article['url']].append(article['tag'])
        article_list = []

        relatedtopics = list(set(filter(lambda y: (len(y)>5) and (len(y)<40), map(lambda x: x[0], Counter(articletagslist).most_common(40)) + filter(lambda x: x in relevanttags, articletagslist))))

        for article in articles:

                domain = urlparse.urlparse(article['url'])[1]
                try:
                        articlesummary = ArticleSemantics.objects.filter(url=article['url']).values('summary')[0]['summary']
                except:
                        articlesummary = None

                try:
			if articlesummary:
	                        articletags = filter(lambda x: x in relatedtopics, articletagsdump2[article['url']])[:5]
			else:
				articletags = []
                except:
                        articletags = []
		
		if articlesummary:
			article_list.append(dict( article, **{'domain': domain, 'articlesummary' : articlesummary, 'tags': articletags}))

        context = RequestContext(request, {
                'articles' : article_list,
                'tagname': tagname,
                'relatedtopics': relatedtopics,
                'title': title,
                'h1title': h1title,
		'canonicalurl': 'http://www.zippednews.com/crsqtrending/'+topic+'/'+topicname
        })

        if request.mobile:
                template = loader.get_template('crsq/zippednewsapp/tagpagemobile2.html')
        else:
                template = loader.get_template('crsq/zippednewsapp/tagpage.html')

        return HttpResponse(template.render(context))

def zippednewsapp(request, tag):
	tag = tag.lower()
	if ArticleTags.objects.filter(tag=tag).count()>0:
		ztv = ZnTagVisit(tag=tag)
		ztv.save()
	try:
		if 'elasticsearchfail' in request.GET.keys():
			if request.GET['elasticsearchfail']=="True":
				raise
		searchterm = tag.replace('-',' ').title()
		searchterm2 = '"' + searchterm + '" ' + searchterm
		urls = article_elastic_search.searchdoc(searchterm2, num=12, recencyweight=7.5)
		urls = map(lambda y: y['url'], filter(lambda x: not ((x['summary'] == None) or (x['summary'] == '')), ArticleSemantics.objects.filter(url__in=urls).values()))
		urls = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=urls).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:9])
	except:
		# Elastic Search Failed
		urls = map(lambda x: x['url'], ArticleTags.objects.filter(tag=tag).values('url'))
		urls = map(lambda x: x['url'], ArticleSemantics.objects.filter(url__in=urls).exclude(summary=None).exclude(summary='').values('url'))
		urls = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=urls).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:9])

	if tag in ["gabi-grecko", "breasts", "porn", "jihadi"]:
		urls= []
	if filter(lambda x: x in tag, ["breast", "porn", "sex-", "nude-", "portioli", "-sex", "hot-pics", "jihadi", "-nude", "penis", "vagina", "pelvic", "nudity", "arrested-for"]):
		urls = []

	urls = filter(lambda x: not 'dailymail.co.uk' in x, urls)

        if request.mobile:
                urls = urls[:5]
        else:
                urls = urls[:8]

	if len(urls)==0:
		ArticleTags.objects.filter(tag=tag).delete()

	title = '"' + tag.replace('-',' ').title() + '"' + " - Latest news on " + '"' + tag.replace('-',' ').title() + '"' + " - ZippedNews"
	h1title = "\"" + tag.replace('-',' ').title() + "\" - Latest news"

	articles = ArticleInfo.objects.filter(url__in=urls).order_by('-id').values()
	articletagsdump = ArticleTags.objects.filter(url__in=urls).values()
	articletagsdump2 = collections.defaultdict(list)
	articletagslist = list(set(map(lambda x: x['tag'], articletagsdump)))
	for article in articletagsdump:
		articletagsdump2[article['url']].append(article['tag'])
	article_list = []

	relatedtopics = list(set(filter(lambda y: (len(y)>5) and (len(y)<40), map(lambda x: x[0], Counter(articletagslist).most_common(50)) + filter(lambda x: x in relevanttags, articletagslist))))

	for article in articles:

		domain = urlparse.urlparse(article['url'])[1]
		try:
                	articlesummary = ArticleSemantics.objects.get(url=article['url']).summary
		except:
                	articlesummary = None

	        try:
			if articlesummary:
				articletags = filter(lambda x: x in relatedtopics, articletagsdump2[article['url']])[:10]
			else:
				articletags = []
	        except:
        	        articletags = []

		if articlesummary:
			if 'nude' not in article['articletitle']:
				article_list.append(dict( article, **{'domain': domain, 'articlesummary' : articlesummary, 'tags': articletags}))

        context = RequestContext(request, {
                'articles' : article_list,
                'tagname': tag,
		'relatedtopics': relatedtopics[:20],
		'title': title,
		'h1title': h1title,
		'canonicalurl': 'http://www.zippednews.com/'+tag,
		'indexallowed': getIndexAllowed(tag)
        })

	if request.mobile:
		template = loader.get_template('crsq/zippednewsapp/tagpagemobile2.html')
	else:
		template = loader.get_template('crsq/zippednewsapp/tagpage.html')

        return HttpResponse(template.render(context))

def zippednewsapptaglist(request, tagsearch):

	taglist = filter(lambda x: x.find(tagsearch)==0, relevanttags)
        template = loader.get_template('crsq/zippednewsapp/taglist.html')
        context = RequestContext(request, {
                'taglist': sorted(taglist),
		'tagsearch': tagsearch
        })

        return HttpResponse(template.render(context))

def zippednewszninput(request):
	html=""

	if 'update' in request.GET.keys():
		ZnInputTag.objects.all().delete()
		l = request.GET['reporting_live_list'].split(',')
		for tag in l:
			zn = ZnInputTag()
			zn.heading = 'reporting_live_list'
			zn.tag = tag
			zn.save()
                l = request.GET['movie_review_list'].split(',')
                for tag in l:
                        zn = ZnInputTag()
                        zn.heading = 'movie_review_list'
                        zn.tag = tag
                        zn.save()
                l = request.GET['popular_traffic_sources'].split(',')
                for tag in l:
                        zn = ZnInputTag()
                        zn.heading = 'popular_traffic_sources'
                        zn.tag = tag
                        zn.save()

	if 'view' in request.GET.keys() or 'update' in request.GET.keys():
                html += "<br/>reporting_live_list<br/><textarea form='zninputform' rows=5 cols=50 id='reporting_live_list' name='reporting_live_list'>"
		tags = ZnInputTag.objects.filter(heading='reporting_live_list').values_list('tag', flat=True)
                html += ",".join(tags) + "</textarea>"
                html += "<br/>movie_review_list<br/><textarea form='zninputform' rows=5 cols=50 id='movie_review_list' name='movie_review_list'>"
		tags = ZnInputTag.objects.filter(heading='movie_review_list').values_list('tag', flat=True)
                html += ",".join(tags) + "</textarea>"
                html += "<br/>popular_traffic_sources<br/><textarea form='zninputform' rows=5 cols=50 id='popular_traffic_sources' name='popular_traffic_sources'>"
		tags = ZnInputTag.objects.filter(heading='popular_traffic_sources').values_list('tag', flat=True)
                html += ",".join(tags) + "</textarea>"
		html += "<form id='zninputform' action='/zippednewszninput'><input type='text' value='1' id='update' name='update'/><input type='submit' value='Update'/></form>"


	return HttpResponse(html)
	
def zippednewsappwelcome(request):

	if 'topicsearch' in request.GET.keys():
		return redirect('http://www.zippednews.com/' + slugify(request.GET['topicsearch']))

	googletrendsfile = open(settings.BASE_DIR+'/crsq/static/crsq/data/tags/googletrendstags.txt', 'r')
	google_trends = pickle.load(googletrendsfile)
	
	def positioning(loc):
		p = ['US', 'India', 'UK', 'Australia']
		try:
			return p.index(loc)
		except:
			return len(p)

	gt = sorted(google_trends.items(), key=lambda x: positioning(x[0]))
	
	imagedict = {}
	topics = filter(lambda x: ((len(x)>5) and (x[0].isdigit()==False)), sorted(list(set(google_trends['US'] + google_trends['India']))))
	for topic in topics:
		imagedict[topic] = dbcache.getAppropriateImageTag(topic)
	for topic in ["t", "s", "snc", "m", "w", "b", "e", "p"]:
		imagedict["zippednewscrsq"+topic] = dbcache.getAppropriateImageTopic(topic)
	
        if request.mobile:
                template = loader.get_template('crsq/zippednewsapp/welcomemobile.html')
        else:
                template = loader.get_template('crsq/zippednewsapp/welcome.html')

        context = RequestContext(request, {
		'google_trends': gt,
		'google_trends_mobile': filter(lambda x: ((len(x)>5) and (x[0].isdigit()==False)), list(set(google_trends['US'] + google_trends['India']))),
		'topicimages': imagedict.items(),
		'reporting_live_list': ZnInputTag.objects.filter(heading='reporting_live_list').values_list('tag', flat=True),
		'movie_review_list': ZnInputTag.objects.filter(heading='movie_review_list').values_list('tag', flat=True),
		'popular_traffic_sources': ZnInputTag.objects.filter(heading='popular_traffic_sources').values_list('tag', flat=True),
        })

        return HttpResponse(template.render(context))

##########################################################################################
##########################################################################################
##########################################################################################

def viewwhatistrending(request):

    try:
        typeofrequest = request.GET.get('typeofrequest')
    except:
        typeofrequest = ''

    if typeofrequest in ['google', 'trends']:
        gt = whatistrending.google_trends.get_all_google_trends().items()
    else:
        gt = None

    if typeofrequest in ['twitter', 'trends']:
        tt = whatistrending.twitter_trends.get_all_twitter_trends().items()
    else:
        tt = None

    if typeofrequest in ['youtube', 'trends']:
        yt = whatistrending.youtube_trends.get_all_youtube_trends().items()
    else:
        yt = None

    if typeofrequest in ['topic']:
        topic = request.GET.get('topic')
        qp = whatistrending.search.get_quora_page(topic)
        tp = whatistrending.search.get_twitter_page(topic)
        th = whatistrending.search.get_twitter_handles_from_topic(topic)
    else:
        (qp, tp, th) = (None, None, None)

    context = RequestContext(request, {
	'gt': gt,
	'tt': tt,
	'yt': yt,
	'qp': qp,
	'tp': tp,
	'th': th
    })

    template = loader.get_template('crsq/whatistrending/index.html')

    return HttpResponse(template.render(context))

def whatistrendingwhattowrite(request):

    def validkeyword(keyword, constraint):
        searchterm2 = '"' + keyword + '" ' + keyword
        urls = article_elastic_search.searchdoc(searchterm2, 15, recencyweight=20.0)
        urls = list(set(sum(map(lambda x: map(lambda y: y['url'], ArticleInfo.objects.filter(url__in=urls).filter(articlecontent__icontains=x).values('url')), constraint['wordlist']), [])))
        if len(urls)>5:
            return True
        else:
            return False
    
    trends = [
	{'country': 'India', 'sector': 'Business', 'topics': whatistrending.google_trends.get_google_trends_topic_location('in','b')},
        {'country': 'India', 'sector': 'Technology', 'topics': whatistrending.google_trends.get_google_trends_topic_location('in','tc')}, 
        {'country': 'U.S.', 'sector': 'Business', 'topics': whatistrending.google_trends.get_google_trends_topic_location('us','b')}, 	
        {'country': 'U.S.', 'sector': 'Technology', 'topics': whatistrending.google_trends.get_google_trends_topic_location('us','tc')}, 
	]

    pristine_constraints = {'wordlist': ['venture', 'pe firm', 'equity', 'stock market', 'stock exchange', 'share price', 'valuation', 'earning', 'market price', 'investor', 'acquisition'] }

    pristine_valid_keywords = filter(lambda y: validkeyword(y, pristine_constraints), list(set(sum((map(lambda x: x['topics'], trends)),[]))))
    
    context = RequestContext(request, {
	'trends': trends,
	'pristine_valid_keywords': pristine_valid_keywords,
    })

    template = loader.get_template('crsq/whatistrending/whattowrite.html')

    return HttpResponse(template.render(context))


##########################################################################################
##########################################################################################
##########################################################################################
	
def dbchecker(request, extraparam=0):

	if extraparam.isdigit():
		startingpoint = int(extraparam)

		articleurldates = ArticleInfo.objects.all().order_by('-id')[startingpoint*200:startingpoint*200+200].values('url', 'articledate')
	
		context = RequestContext(request, {
			'articleurldates': articleurldates
		})

		html = "<html><body><table>"

		for aud in articleurldates:
			if aud['articledate']:
				html+= "<tr><td style='width:70%'><a href='" + aud['url']+ "'>"+aud['url']+"</a></td><td style='width:30%'>"+aud['articledate'].strftime("%B %d, %Y") + "</td></tr>"

		html += "</table></body></html>"

        return HttpResponse(html)

##########################################################################################
##########################################################################################
##########################################################################################


def emailrecommender(request, emailhash):

	if EmailInfo.objects.filter(emailhash=emailhash).count()==0:
	        return HttpResponse("<html><body>Email Recommender - Wrong Input</body></html>")

	e = EmailInfo.objects.filter(emailhash=emailhash).values()[0]

	if len(EmailInfo.objects.get(emailhash=emailhash).cleanbody)<50:
		recommendedemails = []
		recommendedlinks = []
		recommendedlinks_from_introduction = []
		recommendedpeople = []
		reviewlinks = ''

	else:
		try:
			ehashes = email_elastic_search.recommendedemails(emailhash)
		except:
			ehashes = []

		recommendedemails = []
		for ehash in ehashes[:5]:
			subject = map(lambda x: x['subject'], EmailInfo.objects.filter(emailhash=ehash).values('subject'))
			recommendedemails.append((subject, ehash))

		recommendedlinks = article_elastic_search.searchdoc(e['tags'].replace('-',' ').title(), num=30, threshold=0.55, recencyweight=0.0)
		recommendedlinks = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=recommendedlinks).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:15])
	
		#introtags = re.compile(r'<[^>]+>').sub('', e['introductiontags'])
		#introtags = ' '.join(map(lambda y: '"'+y.strip()+'"', filter(lambda x: len(x.strip().split(' '))>1, introtags.split(','))))
		introtags = ' '.join(filter(lambda y: y, map(lambda x: x[0], emailstr2tuples(e['introductiontags']))))
		recommendedlinks_from_introduction = article_elastic_search.searchdoc(introtags, num=10, threshold=2.5, recencyweight=1.0)

		recommendedpeople = relatedemailaddr(e)

		try:
			loclist = json.loads(e['eventtags2'])['locationtags']
			locationtags = urllib2.quote(' '.join(loclist))
			if locationtags == '':
				reviewlinks = ''
			else:
				reviewlinks = 'http://www.asklaila.com/search/Bangalore/-/' + locationtags + '/?searchNearby=false'
		except Exception as exc:
			logger.exception(exc)
			reviewlinks = ''

	template = loader.get_template('crsq/emailrecommender/index.html')
        context = RequestContext(request, {
                'e': e,
		'recommendedemails': recommendedemails,
		'recommendedlinks': recommendedlinks,
		'recommendedlinks_from_introduction': recommendedlinks_from_introduction,
		'recommendedpeople': recommendedpeople,
		'reviewlinks': reviewlinks
        })

        return HttpResponse(template.render(context))

##########################################################################################
##########################################################################################
##########################################################################################
	
def zopeyesearch(request, keywordstr):

	if keywordstr.strip() == "":
		return HttpResponse("<html><body>Zop Eye Search - Wrong Input</body></html>")

	"""
        tags = text_summarize.text_summarize.get_text_tags(keywordstr)
        tags = ' '.join(tags).strip()
        if tags == '':
                urldicts = []
        else:
		urldicts = article_elastic_search.searchdoc(tags, highlight=True, num=20)
	"""

	urldicts = article_elastic_search.searchdoc(keywordstr, highlight=True, num=50)
	
	clustered_urls = article_elastic_search.searchdoc_clusters(map(lambda x: x['url'], urldicts), keywordstr)
	res = []
	for clust in clustered_urls:
		tempresult= []
		for url in clust:
			article = ArticleInfo.objects.get(url=url)
			urldict = filter(lambda x: x['url']==url, urldicts)[0]
			urldict['image'] = article.articleimage
			urldict['domain'] = article.domainname()
			urldict['title'] = article.articletitle
			if urldict['image']:
				tempresult.append(urldict)
		if tempresult:
			res.append(tempresult)
	res = sorted(res, key=lambda x: -len(x))
	return HttpResponse(json.dumps(res), content_type="application/json")

##########################################################################################
##########################################################################################
##########################################################################################

def crsqsemanticsimilarityapi(request, param1, param2):

	# Will be true if the same IP makes more than rate.
	was_limited = getattr(request, 'limited', False)

        param1 = param1.lower()
        param2 = param2.lower()

	if was_limited:
		result = {'param1': param1, 'param2': param2, 'error': 'Limit per minute exceeded. Contact pratikpoddar05051989@gmail.com to get unlimited access to the api' }
		
	else:
		result = {'param1': param1, 'param2': param2, 'closeness': article_elastic_search.semantic_closeness_webdice(param1, param2)}
	
	return HttpResponse(json.dumps(result), content_type="application/json")

def crsqsemanticsimilarity(request):

	if ('param1' in request.GET.keys()) and ('param2' in request.GET.keys()):
		param1 = request.GET['param1']
		param2 = request.GET['param2']
		closeness = article_elastic_search.semantic_closeness_webdice(param1, param2)
	else:
		closeness = ''
		param1 = ''
		param2 = ''
	

        template = loader.get_template('crsq/crsqsemanticsimilarity/index.html')
        context = RequestContext(request, {
                'closeness': closeness,
                'param1': param1,
		'param2': param2
        })
        return HttpResponse(template.render(context))


##########################################################################################
##########################################################################################
##########################################################################################

