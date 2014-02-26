from django.conf.urls import patterns, include, url
from crsq import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='default'),

	url(r'^content-affiliate-advertising/?$', views.caa, name='caa'),

	url(r'^twitter-newspaper/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/?$', views.tw_np, name='tw_np'),
	url(r'^twitter-newspaper/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([0-9]+)/?$', views.tw_np, name='tw_np'),
	url(r'^twitter-newspaper', views.tw_np_redirect, name='tw_np_redirect'),

	url(r'^timeline-news/article/[a-zA-Z0-9-]+/([0-9]+)/?$', views.timenews_article, name='timenews_article'),
	url(r'^timeline-news/([a-zA-Z0-9-]+)/?$', views.timenews, name='timenews'),

	url(r'^penpatron/?$', views.penp, name='penp'),
	url(r'^penpatron-message/?$', views.penpmessage, name='penpmessage'),

        url(r'^linkbook/?$', views.linkbook_view, name='linkbook'),

	url(r'^zippednewsapp/?$', views.zippednewsappwelcome, name='znw'),
	url(r'^zippednewsapp/crsqsearch/([a-zA-Z0-9-]+)/?$', views.zippednewsapptaglist, name='zntl'),
	url(r'^zippednewsapp/([a-zA-Z0-9-]+)/?$', views.zippednewsapp, name='zn'),

	url(r'^dbchecker/([a-zA-Z0-9]+)/?$', views.dbchecker, name='dbsummarychecker')
)


