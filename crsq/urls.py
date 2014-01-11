from django.conf.urls import patterns, include, url
from crsq import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='default'),
	url(r'^content-affiliate-advertisin', views.caa, name='caa'),
)


