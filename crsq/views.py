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
from crsq.twitter_newspaper import twitter_newspaper
from crsq.models import ArticleInfo


logger = logging.getLogger(__name__)

tw_np_sector_list = ["Technology", "Politics", "Entertainment", "Sports", "Business", "Travel"]
tw_np_location_list = ["World", "United States", "India", "San Francisco, USA", "Los Angeles, USA", "New York, USA", "Boston, USA", "London, UK", "Mumbai, India", "Bangalore, India", "New Delhi, India", "Singapore"]


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

def tw_np(request, sector, location):

	if (not filter(lambda x: slugify(x)==sector, tw_np_sector_list)) or (not filter(lambda x: slugify(x)==location, tw_np_location_list)):
		return HttpResponse("<html><body>Twitter Newspaper - Wrong Input</body></html>")

	template = loader.get_template('crsq/twitter-newspaper/index.html')
	articles = twitter_newspaper.get_articles(sector, location)
	context = RequestContext(request, {
	        'article_list': map(lambda x: dict( x, **{'domain': urlparse.urlparse(x['url'])[1]} ), articles[0:10]),
		'sector': sector,
		'sectorname': filter(lambda x: slugify(x)==sector, tw_np_sector_list)[0],
		'location': location,
		'locationname': filter(lambda x: slugify(x)==location, tw_np_location_list)[0],
		'sector_list': tw_np_sector_list,
		'location_list': tw_np_location_list
        })
	return HttpResponse(template.render(context))	

def tw_np_redirect(request):
	return redirect('/twitter-newspaper/technology/india')



