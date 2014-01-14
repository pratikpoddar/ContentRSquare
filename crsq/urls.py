from django.conf.urls import patterns, include, url
from crsq import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='default'),
	url(r'^content-affiliate-advertising$', views.caa, name='caa'),
	url(r'^twitter-newspaper/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)$', views.tw_np, name='tw_np'),
	url(r'^twitter-newspaper', views.tw_np_redirect, name='tw_np_redirect'),
)


