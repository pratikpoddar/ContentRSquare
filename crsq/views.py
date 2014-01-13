from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from django.templatetags.static import static
from django.db.models import Count

import urllib
from datetime import datetime
from datetime import timedelta
from datetime import date
import pytz

import logging
import urlparse
from crsq.content_affiliate_advertising import content_affiliate_advertising
from crsq.models import ArticleInfo

logger = logging.getLogger(__name__)

def index(request):
	now = datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

def caa(request):

	logger.debug(request.GET.keys())

	if filter(lambda x: x not in request.GET.keys(), ['text','index','jsonp_callback']):
		return HttpResponse("<html><body>Content Affiliate Advertising - Wrong Input</body></html>")

	keywords = content_affiliate_advertising.content_affiliate(request.GET['text'], request.GET['index']) 
	#keywords = [{'keyword':'Columbia Business School', 'link':'http://www.cseblog.com'}]

        jsonresponse = request.GET['jsonp_callback'] + '({"keywords":' + str(keywords) + '})'
	
        return HttpResponse(jsonresponse)

def twitter_newspaper(request):

	template = loader.get_template('crsq/twitter-newspaper/index.html')
	context = RequestContext(request, {
	        'article_list': map(lambda x: dict( x, **{'domain': urlparse.urlparse(x['url'])[1]} ), ArticleInfo.objects.all().values('url', 'articletitle', 'articlecontent', 'articleimage', 'twitterpower', 'fbpower'))
        })
	return HttpResponse(template.render(context))	


