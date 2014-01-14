from crsq.twitter_newspaper import twitter_newspaper
from crsq.models import ArticleInfo, TweetLinks
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_articles():
	tl = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))
	ai = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
	tobeexpanded = list(set(tl)-set(ai))

	for l in tobeexpanded:
		twitter_newspaper.put_article_details(l)
	return

def run_twitter_newspaper(sector, tuser, tlist):
	print sector + ' ' + tuser + ' ' + tlist
	logger.debug('run_twitter_newspaper - Getting Twitter Newspaper Result ' + sector + tuser + tlist)
	twitter_newspaper.get_list_timeline(sector, tuser, tlist, 200)
	get_articles()
	return

toberun = int(datetime.now().hour) % 4
if toberun == 0:
	run_twitter_newspaper('technology', 'pratikpoddar', 'startups')
if toberun == 1:
	run_twitter_newspaper('technology', 'dkhare', 'india-tech-and-vc')
if toberun == 2:
	run_twitter_newspaper('technology', 'Scobleizer', 'tech-news-people')
if toberun == 3:
	run_twitter_newspaper('entertainment', 'tellychakkar', 'celebs')

