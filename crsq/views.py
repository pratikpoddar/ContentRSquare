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

import logging
import urlparse
import json
from crsq.content_affiliate_advertising import content_affiliate_advertising
from crsq.twitter_newspaper import twitter_newspaper
from crsq.linkbook import linkbook
from crsq.models import ArticleInfo, PenPatronUser, ArticleSemantics, ArticleTags


logger = logging.getLogger(__name__)

tw_np_sector_list = ["Technology", "Politics", "Entertainment", "Sports", "Business"]
tw_np_location_list = ["World", "United States", "India", "San Francisco, USA", "Los Angeles, USA", "New York, USA", "Boston, USA", "London, UK", "Mumbai, India", "Bangalore, India", "New Delhi, India", "Singapore"]
tw_np_location_list = ["World"]


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

	if (not filter(lambda x: slugify(x)==sector, tw_np_sector_list)) or (not filter(lambda x: slugify(x)==location, tw_np_location_list)):
		return HttpResponse("<html><body>Twitter Newspaper - Wrong Input</body></html>")

	articles = twitter_newspaper.get_articles(sector, location)[int(page)*10-10:int(page)*10]

	template = loader.get_template('crsq/twitter-newspaper/index.html')

	context = RequestContext(request, {
	        'article_list': map(lambda x: dict( x, **{'domain': urlparse.urlparse(x['url'])[1], 'sharers': twitter_newspaper.get_sharers(x['url'])} ), articles),
		'sector': sector,
		'sectorname': filter(lambda x: slugify(x)==sector, tw_np_sector_list)[0],
		'location': location,
		'locationname': filter(lambda x: slugify(x)==location, tw_np_location_list)[0],
		'sector_list': tw_np_sector_list,
		'location_list': tw_np_location_list,
		'page': int(page),
		'pagerange' : range(max(1,int(page)-2),max(1,int(page)-2)+5)
        })
	return HttpResponse(template.render(context))

def linkbook_view(request):

	sharer="Zlemma Inc"
	topic = "Tech Fuck"

        articles = linkbook.get_linkbook_articles(sharer, topic)

        template = loader.get_template('crsq/linkbook/index.html')

        context = RequestContext(request, {
                'article_list': articles,
		'sharername': "Zlemma Inc",
		'sharerlink': "http://www.zlemma.com",
		'sharertopic': "Technology Articles",
		'sharerquote': "Technology is changing and you know it. Lets change with it. F. G. H. I.",
		'sharerimage': "http://www.zlemma.com/static/common/img/logo.png"
        })
        return HttpResponse(template.render(context))
	

def tw_np_article(request, articleid):
	
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

        template = loader.get_template('crsq/twitter-newspaper/article.html')

        context = RequestContext(request, {
		'article' : dict( article, **{'domain': domain, 'sharers': sharers, 'articlesummary' : articlesemantics['summary'], 'topic': articlesemantics['topic'], 'tags': ', '.join(articletags)})
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

	



