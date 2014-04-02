from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from django.templatetags.static import static
from django.db.models import Count

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

from crsq.crsqlib import article_elastic_search, email_elastic_search

from dateutil.parser import parse as dateutilparse

import collections

import random

logger = logging.getLogger(__name__)

relevanttags = dbcache.getRelevantTags()

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

def gmailemailjs(request):

	def getemailaddr(string):
		return filter(lambda x: x.find('@')>0, string.split(' '))[-1].strip()

	def getemailhash(username, fromaddr, subject, dateemail):

		try:
			return EmailInfo.objects.filter(user__contains=username, emailfrom__contains=fromaddr, subject__contains=subject, emailtime__range=(dateemail-timedelta(minutes=2),dateemail+timedelta(minutes=1))).values('emailhash')[0]['emailhash']
		except Exception as exc:
			logger.exception(exc)
			return []

	emailidentifier = request.GET['emailidentifier']
	username = request.GET['username']
	offset = timedelta(hours=5, minutes=30)
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
		emailhashes += [getemailhash(username, fromaddr, subject, dateemail)]
		
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

                domain = urlparse.urlparse(article['url'])[1]
                try:
                        articlesemantics = ArticleSemantics.objects.filter(url=article['url']).values('summary')[0]
                except Exception as e:
			logger.exception(e)
                        articlesemantics = {'summary': None}

                article_list.append(dict( article, **{'domain': domain, 'articlesummary' : articlesemantics['summary'], 'sharers': twitter_newspaper.get_sharers(article['url'])}))

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
	try:
		logger.debug(request.GET.keys())
		if 'elasticsearchfail' in request.GET.keys():
			if request.GET['elasticsearchfail']=="True":
				raise
                urls = article_elastic_search.searchdoc(tag.replace('-',' ').title(), 30)
                urls = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=urls).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:15])
	except:
		# Elastic Search Failed
		urls = map(lambda x: x['url'], ArticleTags.objects.filter(tag=tag).values('url'))
		urls = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=urls).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:15])

	articles = ArticleInfo.objects.filter(url__in=urls).values()

	articletagsdump = ArticleTags.objects.filter(url__in=urls).values('tag', 'url')
	articletagsdump2 = collections.defaultdict(list)
	for article in articletagsdump:
		articletagsdump2[article['url']].append(article['tag'])

	
	articles = sorted(articles, key=lambda article: -article['id'])
	article_list = []
	
	for article in articles:

		domain = urlparse.urlparse(article['url'])[1]
		try:
                	articlesemantics = ArticleSemantics.objects.filter(url=article['url']).values('summary', 'topic')[0]
		except:
                	articlesemantics = {'summary': None, 'topic': None}

	        try:
			articletags = articletagsdump2[article['url']]
			#articletags = filter(lambda x: x in relevanttags, articletagsdump2[article['url']])
        	        #articletags = map(lambda x: x['tag'], ArticleTags.objects.filter(url=article['url']).values('tag'))
			#articletags = filter(lambda x: x in relevanttags, articletags)
	        except:
        	        articletags = []

		article_list.append(dict( article, **{'domain': domain, 'articlesummary' : articlesemantics['summary'], 'topic': articlesemantics['topic'], 'tags': articletags}))

        context = RequestContext(request, {
                'articles' : article_list,
                'tag': tag
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

	googletrendsfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/googletrendstags.txt', 'r')
	google_trends = pickle.load(googletrendsfile)
	
	def positioning(loc):
		p = ['India', 'US', 'UK']
		try:
			return p.index(loc)
		except:
			return len(p)

	gt = sorted(google_trends.items(), key=lambda x: positioning(x[0]))

	template = loader.get_template('crsq/zippednewsapp/welcome.html')
        context = RequestContext(request, {
		'google_trends': gt
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

	if len(EmailInfo.objects.get(emailhash=emailhash).cleanbody)<50:
		return HttpResponse("<html><body>Email Recommender - Too short an email</body></html>")

	e = EmailInfo.objects.filter(emailhash=emailhash).values()[0]
	ehashes = email_elastic_search.recommendedemails(emailhash)
	recommendedemails = []
	for ehash in ehashes[:5]:
		subject = map(lambda x: x['subject'], EmailInfo.objects.filter(emailhash=ehash).values('subject'))
		recommendedemails.append((subject, ehash))

	recommendedlinks = article_elastic_search.searchdoc(e['tags'].replace('-',' ').title(), num=30, threshold=0.25, weightfrontloading=20.0, recencyweight=0.0)
	recommendedlinks = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=recommendedlinks).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:15])
	
	introtags = re.compile(r'<[^>]+>').sub('', e['introductiontags'])
	introtags = ' '.join(map(lambda y: '"'+y.strip()+'"', filter(lambda x: len(x.strip().split(' '))>1, introtags.split(','))))
	recommendedlinks_from_introduction = article_elastic_search.searchdoc(introtags, num=10, threshold=0.3, recencyweight=1.0)

	try:
		loclist = json.loads(e['eventtags2'])['locationtags']
		locationtags = urllib2.quote(' '.join(loclist))
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
		'reviewlinks': reviewlinks
        })

        return HttpResponse(template.render(context))
	

	





	







