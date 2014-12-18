from django.conf.urls import patterns, include, url
from crsq import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='default'),

	url(r'^content-affiliate-advertising/?$', views.caa, name='caa'),

	url(r'^what-is-trending/?$', views.viewwhatistrending, name='whatistrending'),

	url(r'^twitterstreetjournal/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/?$', views.tw_np, name='tw_np'),
	url(r'^twitterstreetjournal/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([0-9]+)/?$', views.tw_np, name='tw_np'),
	url(r'^twitterstreetjournal', views.tw_np_redirect, name='tw_np_redirect'),

	url(r'^zippednewsapp/?$', views.zippednewsappwelcome, name='znw'),
	url(r'^zippednewsapp/crsqsearch/([a-zA-Z0-9-]+)/?$', views.zippednewsapptaglist, name='zntl'),
        url(r'^zippednewsapp/crsqtrending/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/?$', views.zippednewsapptrending, name='zntp'),
	url(r'^zippednewsapp/([a-zA-Z0-9-]+)/?$', views.zippednewsapp, name='zn'),

        url(r'^crsqsemanticsimilarityapi/([a-zA-Z0-9 ]+)/([a-zA-Z0-9 ]+)/?$', views.crsqsemanticsimilarityapi, name='crsqssapi'),
        url(r'^crsqsemanticsimilarity/?$', views.crsqsemanticsimilarity, name='crsqss'),

        url(r'^timeline-news/article/[a-zA-Z0-9-]+/([0-9]+)/?$', views.timenews_article, name='timenews_article'),
        url(r'^timeline-news/([a-zA-Z0-9-]+)/?$', views.timenews, name='timenews'),

	url(r'^emailrecommender/([a-zA-Z0-9]+)/?$', views.emailrecommender, name='emailrecommender'),
	url(r'^zopeyesearch/([a-zA-Z0-9 ]+)/?$', views.zopeyesearch, name='zopeyesearch'),

        url(r'^dbchecker/([a-zA-Z0-9]+)/?$', views.dbchecker, name='dbsummarychecker'),

        url(r'^gmailemailjs/?$', views.gmailemailjs, name='gmailemailjs'),	
	url(r'^gmailemailjs_imap/?$', views.gmailemailjs_imap, name='gmailemailjs_imap'),

)


