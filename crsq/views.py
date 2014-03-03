from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from django.templatetags.static import static
from django.db.models import Count

from django.core.context_processors import csrf

import urllib
import urllib2
from datetime import datetime
from datetime import timedelta
from datetime import date
import pytz
import pickle
import logging
import urlparse
import json
from crsq.content_affiliate_advertising import content_affiliate_advertising
from crsq.twitter_newspaper import twitter_newspaper
from crsq.linkbook import linkbook
from crsq import dbcache
from crsq.models import ArticleInfo, PenPatronUser, ArticleSemantics, ArticleTags, ImportantTags

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

	template = loader.get_template('crsq/twitter-newspaper/index.html')

	context = RequestContext(request, {
	        'article_list': article_list,
		'sector': sector,
		'sectorname': filter(lambda x: slugify(x)==sector, twitter_newspaper.tw_np_sector_list)[0],
		'location': location,
		'locationname': filter(lambda x: slugify(x)==location, twitter_newspaper.tw_np_location_list)[0],
		'sector_list': twitter_newspaper.tw_np_sector_list,
		'location_list': twitter_newspaper.tw_np_location_list,
		'page': int(page),
		'pagerange' : range(max(1,int(page)-2),max(1,int(page)-2)+5)
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
	return redirect('/twitter-newspaper/technology/world')

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

	urls = map(lambda x: x['url'], ArticleTags.objects.filter(tag=tag).values('url'))
	urls = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=urls).exclude(articleimage='').exclude(articleimage=None).order_by('-id').values('url')[:15])
	articles = ArticleInfo.objects.filter(url__in=urls).order_by('-id').values()

	articletagsdump = ArticleTags.objects.filter(url__in=urls).values('tag', 'url')
	articletagsdump2 = collections.defaultdict(list)
	for article in articletagsdump:
		articletagsdump2[article['url']].append(article['tag'])
	
	article_list = []
	
	for article in articles:

		domain = urlparse.urlparse(article['url'])[1]
		try:
                	articlesemantics = ArticleSemantics.objects.filter(url=article['url']).values('summary', 'topic')[0]
		except:
                	articlesemantics = {'summary': None, 'topic': None}

	        try:
			articletags = filter(lambda x: x in relevanttags, articletagsdump2[article['url']])
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

	taglist = filter(lambda x: x.find(tagsearch)==0, dbcache.getRelevantTags())
        template = loader.get_template('crsq/zippednewsapp/taglist.html')
        context = RequestContext(request, {
                'taglist': sorted(taglist),
		'tagsearch': tagsearch
        })

        return HttpResponse(template.render(context))


	
def zippednewsappwelcome(request):

	googletrendsfile = open('/home/ubuntu/crsq/crsq/static/crsq/data/tags/googletrendstags.txt', 'r')
	google_trends = pickle.load(googletrendsfile)

	#tagdict = {}
	#tagdict = dbcache.getRelevantTagDict()

	#recent_articles = ArticleInfo.objects.exclude(articleimage='').exclude(articleimage=None).order_by('-id')[1:4].values()
	#popular_articles = ArticleInfo.objects.exclude(articleimage='').exclude(articleimage=None).order_by('-id')[4:7].values()
	##recent_articles = [ recent_articles[i] for i in sorted(random.sample(xrange(len(recent_articles)), 3)) ]
	##popular_articles = [ popular_articles[i] for i in sorted(random.sample(xrange(len(popular_articles)), 3)) ]

	def summary(url):
		try:
			return ArticleSemantics.objects.filter(url=url).values('summary')[0]['summary']
		except:
			return None

	#recent_articles = map(lambda x: dict( x, **{'domain': urlparse.urlparse(x['url'])[1], 'summary': summary(x['url'])} ), recent_articles)
	#popular_articles = map(lambda x: dict( x, **{'domain': urlparse.urlparse(x['url'])[1], 'summary': summary(x['url'])} ), popular_articles)

	template = loader.get_template('crsq/zippednewsapp/welcome.html')
        context = RequestContext(request, {
                #'tagdict': sorted(tagdict.items()),
		'google_trends': sorted(google_trends.items()),
		#'recent_articles': recent_articles,
		#'popular_articles':  popular_articles
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


