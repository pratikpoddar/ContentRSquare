from django.conf.urls import patterns, include, url
from crsq import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='default'),
	url(r'^content-affiliate-advertising', views.caa, name='caa'),
	url(r'^twitter-newspaper', views.twitter_newspaper, name='twitter_newspaper'),
)


