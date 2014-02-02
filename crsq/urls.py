from django.conf.urls import patterns, include, url
from crsq import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='default'),

	url(r'^content-affiliate-advertising/?$', views.caa, name='caa'),

	url(r'^twitter-newspaper/article/[a-zA-Z0-9-]+/([0-9]+)/?$', views.tw_np_article, name='tw_np_article'),
	url(r'^twitter-newspaper/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/?$', views.tw_np, name='tw_np'),
	url(r'^twitter-newspaper/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([0-9]+)/?$', views.tw_np, name='tw_np'),
	url(r'^twitter-newspaper', views.tw_np_redirect, name='tw_np_redirect'),

	url(r'^timeline-news/article/[a-zA-Z0-9-]+/([0-9]+)/?$', views.timenews_article, name='timenews_article'),
	url(r'^timeline-news/([a-zA-Z0-9-]+)/?$', views.timenews, name='timenews'),

	url(r'^penpatron/?$', views.penp, name='penp'),
	url(r'^penpatron-message/?$', views.penpmessage, name='penpmessage'),


)


