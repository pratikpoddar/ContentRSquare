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
from crsq.linkbook import linkbook
from crsq import dbcache
from crsq.models import ArticleInfo, PenPatronUser, ArticleSemantics, ArticleTags, ImportantTags, EmailInfo

from crsq.crsqlib import article_elastic_search, email_elastic_search, text_summarize

from dateutil.parser import parse as dateutilparse

import collections

#from ratelimit.decorators import ratelimit

import random
from crsq.crsqlib.emailutils.emailutils import emailstr2tuples, relatedemailaddr

logger = logging.getLogger(__name__)

relevanttags = dbcache.getRelevantTags()

def loggerdebug(request, string):
	if 'pratik' in request.GET.keys():
		logger.debug(string)
	return

def index(request):
	now = datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

def caa(request):

	if filter(lambda x: x not in request.GET.keys(), ['text','index','jsonp_callback']):
		return HttpResponse("<html><body>Content Affiliate Advertising - Wrong Input</body></html>")

	keywords = content_affiliate_advertising.content_affiliate(request.GET['text'], request.GET['index']) 
	#keywords = [{'keyword':'Columbia Business School', 'link':'http://www.cseblog.com'}]

        jsonresponse = request.GET['jsonp_callback'] + '({"keywords":' + str(keywords) + '})'
	
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

	"""
	openemails = emailidentifier.split(';;||;;||crsq||;;||;;')
	openemails = filter(lambda x: len(x)>0, openemails)
	emailhashes = []
	for openemail in openemails:
		openemailelems = openemail.split('--||--||crsq||--||--')
		fromaddr = getemailaddr(filter(lambda x: x.find('from:')>-1, openemailelems)[0][5:].strip())
		subject = filter(lambda x: x.find('subject:')>-1, openemailelems)[0][8:].strip()
		try:
			dateemail = dateutilparse(filter(lambda x: x.find('date:')>-1, openemailelems)[0][5:].strip())-offset
			dateemail = datetime(dateemail.year, dateemail.month, dateemail.day, dateemail.hour, dateemail.minute, tzinfo=pytz.utc)
		except:
			dateemail = None
		emailhashes += getemailhash(username, fromaddr, subject, dateemail)
	"""
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
		recommendedlinks = article_elastic_search.searchdoc(e['tags'].replace('-',' ').title(), num=30, threshold=0.25, weightfrontloading=20.0, recencyweight=0.0)
	        recommendedlinks = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=recommendedlinks).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:15])
		rlinks += recommendedlinks[:5]

	output = ArticleInfo.objects.filter(url__in=rlinks).values('url', 'articletitle')
	output = json.dumps([dict(x) for x in output])
	
	jsonresponse = request.GET['jsonp_callback'] + '({"output":' + output + '})'
        return HttpResponse(jsonresponse)

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

def linkbook_view(request):

	sharer= {'name': "Zlemma Inc", 'link': "http://www.zlemma.com", 'image': "http://www.zlemma.com/static/common/img/logo.png"}
	topic = "Recruting Industry is Changing"
	quote = "Recruiting industry is evolving rapidly. We are moving towards technical recruitment. Recruiting market is being disrupted using algorithms and big data."
	links = ["http://blogs.hbr.org/2012/10/digital-staffing-the-future-of/", "http://www.forbes.com/sites/georgeanders/2013/04/10/who-should-you-hire-linkedin-says-try-our-algorithm/", "http://www.nytimes.com/2013/04/28/technology/how-big-data-is-playing-recruiter-for-specialized-workers.html", "http://knowledge.wharton.upenn.edu/article/mind-your-social-presence-big-data-recruiting-has-arrived/", "http://www.nytimes.com/2007/01/03/technology/03google.html", "http://www.hackdiary.com/2010/02/10/algorithmic-recruitment-with-github/", "http://proofcommunication.com/proof-to-help-zlemma-the-latest-in-stem-talent-identification/1251"]

        articles = linkbook.get_linkbook_articles(links)

        template = loader.get_template('crsq/linkbook/index.html')

        context = RequestContext(request, {
                'article_list': articles,
		'sharername': sharer['name'],
		'sharerlink': sharer['link'],
		'sharertopic': topic,
		'sharerquote': quote,
		'sharerimage': sharer['image']
        })
        return HttpResponse(template.render(context))
	
def tw_np_redirect(request):
	return redirect('/twitterstreetjournal/technology/san-francisco-usa')

def penp(request, notice=None):

        template = loader.get_template('crsq/penpatron/index.html')
        context = RequestContext(request, {'notice': notice})
	return HttpResponse(template.render(context))

def penpmessage(request):

        if filter(lambda x: x not in request.GET.keys(), ['postName', 'postEmail', 'postPhone', 'postCollege', 'postBlog', 'postMessage']):
		raise Http404

	try:
		ppuser = PenPatronUser(name=request.GET['postName'], email = request.GET['postEmail'], phone = request.GET['postPhone'], college = request.GET['postCollege'], blog = request.GET['postBlog'], message = request.GET['postMessage'])
		ppuser.save()
	except Exception as e:
		logger.exception('views.py - penpmessage - error saving user details - ' + str(e) + ' ' + str(request.GET))
	
	return penp(request, notice="Thanks for your interest. One of our teammates will reach out to you in sometime")
                
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

def zippednewsapp(request, tag):

	if tag=="top-trending":

		loggerdebug(request, 1)
		maxid = ArticleInfo.objects.all().order_by("-id")[0].id
		ai = ArticleInfo.objects.filter(id__gt=maxid-400)
		loggerdebug(request, 2)

		if not(('topic' in request.GET.keys()) and ('name' in request.GET.keys())):
			loggerdebug(request, 3)
			topic = ''
			tag = tag
                        bi = filter(lambda x: (x['source'].find('feedanalyzerfromscratchhttps://news.google.com/')>=0), filter(lambda y: y['source'], ai.values('url', 'source')))
			loggerdebug(request, 4)
		else:
			loggerdebug(request, 5)
			topic = request.GET['topic']
			tag = request.GET['name'].lower()+"-"+tag
			bi = filter(lambda x: (x['source'].find('feedanalyzerfromscratchhttps://news.google.com/')>=0) and (x['source'].endswith('topic='+topic)), filter(lambda y: y['source'], ai.values('url', 'source')))
			loggerdebug(request, 6)

		urls = map(lambda x: x['url'], bi)[-40:]
		random.shuffle(urls)
		urls = urls[:15]
		urls = map(lambda x: x['url'], ArticleSemantics.objects.filter(url__in=urls).exclude(summary=None).exclude(summary='').values('url'))
		urls = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=urls).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:15])
		loggerdebug(request, 7)
	else:
		try:
			loggerdebug(request, 8)
			if 'elasticsearchfail' in request.GET.keys():
				if request.GET['elasticsearchfail']=="True":
					raise
			searchterm = tag.replace('-',' ').title()
			searchterm2 = '"' + searchterm + '"'
	                urls = article_elastic_search.searchdoc(searchterm2, 20)
			if urls==[]:
				searchterm2 = ' AND '.join(searchterm.split(' '))
				urls = article_elastic_search.searchdoc(searchterm2, 20)
				if urls==[]:
					searchterm2 = '"' + searchterm + '" ' + searchterm
					urls = article_elastic_search.searchdoc(searchterm2, 20)
			urls = map(lambda x: x['url'], ArticleSemantics.objects.filter(url__in=urls).exclude(summary=None).exclude(summary='').values('url'))
	                urls = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=urls).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:10])
			loggerdebug(request, 9)
		except:
			# Elastic Search Failed
			urls = map(lambda x: x['url'], ArticleTags.objects.filter(tag=tag).values('url'))
			urls = map(lambda x: x['url'], ArticleSemantics.objects.filter(url__in=urls).exclude(summary=None).exclude(summary='').values('url'))
			urls = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=urls).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:10])

	loggerdebug(request, 10)
	articles = ArticleInfo.objects.filter(url__in=urls).order_by('-id').values()
	loggerdebug(request, 11)
	articletagsdump = ArticleTags.objects.filter(url__in=urls).values('tag', 'url')
	articletagsdump2 = collections.defaultdict(list)
	loggerdebug(request, 12)
	for article in articletagsdump:
		articletagsdump2[article['url']].append(article['tag'])
	loggerdebug(request, 13)
	article_list = []

	relatedtopics = filter(lambda y: (len(y)>5) and (not y in tag) and (not tag in y),map(lambda x: x[0], Counter(sum(articletagsdump2.values(),[])).most_common(40)))
	loggerdebug(request, 14)
	for article in articles:

		domain = urlparse.urlparse(article['url'])[1]
		try:
                	articlesemantics = ArticleSemantics.objects.filter(url=article['url']).values('summary', 'topic')[0]
		except:
                	articlesemantics = {'summary': None, 'topic': None}

	        try:
			articletags = filter(lambda x: x in relatedtopics, articletagsdump2[article['url']])
	        except:
        	        articletags = []

		article_list.append(dict( article, **{'domain': domain, 'articlesummary' : articlesemantics['summary'], 'topic': articlesemantics['topic'], 'tags': articletags}))
	loggerdebug(request, 15)

	if len(article_list)==0:
		return redirect('http://www.zippednews.com')	

        context = RequestContext(request, {
                'articles' : article_list,
                'tag': tag,
		'relatedtopics': relatedtopics[:10]
        })

	if request.mobile:
		template = loader.get_template('crsq/zippednewsapp/tagpagemobile.html')
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


	
def zippednewsappwelcome(request):

	if 'topicsearch' in request.GET.keys():
		return redirect('http://www.zippednews.com/' + slugify(request.GET['topicsearch']))

	googletrendsfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/googletrendstags.txt', 'r')
	google_trends = pickle.load(googletrendsfile)
	
	def positioning(loc):
		p = ['India', 'US', 'UK']
		try:
			return p.index(loc)
		except:
			return len(p)

	gt = sorted(google_trends.items(), key=lambda x: positioning(x[0]))

        if request.mobile:
                template = loader.get_template('crsq/zippednewsapp/welcomemobile.html')
        else:
                template = loader.get_template('crsq/zippednewsapp/welcome.html')

        context = RequestContext(request, {
		'google_trends': gt,
		'google_trends_US': filter(lambda x: ((len(x)>5) and (x[0].isdigit()==False)), sorted(list(set(google_trends['US'] + google_trends['India']))))
        })

        return HttpResponse(template.render(context))
	
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

	if extraparam == "doga":
		articles = ArticleInfo.objects.filter(url__contains="techcrunch.com").values('url', 'articleimage', 'articletitle')
		html = "<html><body>"
		for article in articles:
			html += "<pre>"+str(article)+"</pre><br/>"
		html += "</body></html>"

        return HttpResponse(html)


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

		recommendedlinks = article_elastic_search.searchdoc(e['tags'].replace('-',' ').title(), num=30, threshold=0.55, weightfrontloading=20.0, recencyweight=0.0)
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

#@ratelimit(ip=False, rate='2/m', keys=lambda req: req.META.get('HTTP_X_FORWARDED_FOR', req.META['REMOTE_ADDR']))
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



