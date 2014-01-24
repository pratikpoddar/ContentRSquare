from crsq.twitter_newspaper import twitter_newspaper
from crsq.models import ArticleInfo, TweetLinks, ArticleSemantics
from datetime import datetime
import logging

from django_cron import CronJobBase, Schedule

logger = logging.getLogger(__name__)

def get_articles():
	tl = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))
	ai = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
	tobeexpanded = list(set(tl)-set(ai))

	for l in tobeexpanded:
		twitter_newspaper.put_article_details(l)
	return

def get_article_semantics():
	tl = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))
	asi = map(lambda x: x['url'], ArticleSemantics.objects.all().values('url'))
	tobeexpanded = list(set(tl)-set(asi))

	for l in tobeexpanded[0:2]:
		twitter_newspaper.put_article_semantics(l)
	return

def run_twitter_newspaper(sector, tuser, tlist):
	print sector + ' ' + tuser + ' ' + tlist
	logger.debug('run_twitter_newspaper - Getting Twitter Newspaper Result ' + sector + tuser + tlist)
	twitter_newspaper.get_list_timeline(sector, tuser, tlist, 200)
	get_articles()
	get_article_semantics()
	return

def time_dependent_tw_np(toberun):

	toberun = toberun % 13

	if toberun == 0:
		run_twitter_newspaper('technology', 'pratikpoddar', 'startups')
	if toberun == 1:
		run_twitter_newspaper('technology', 'dkhare', 'india-tech-and-vc')
	if toberun == 2:
		run_twitter_newspaper('technology', 'Scobleizer', 'tech-news-people')
	if toberun == 3:
	        run_twitter_newspaper('technology', 'mashable', 'startups-silicon-valley-24')
	if toberun == 4:
	        run_twitter_newspaper('technology', 'mashable', 'startups-nyc-24')
	if toberun == 5:
	        run_itwitter_newspaper('technology', 'mashable', 'tech')
	if toberun == 6:
	        run_twitter_newspaper('entertainment', 'mashable', 'music')
	if toberun == 7:
		run_twitter_newspaper('entertainment', 'tellychakkar', 'celebs')
	if toberun == 8:
	        run_twitter_newspaper('business', 'WSJ', 'wsj-money')
	if toberun == 9:
	        run_twitter_newspaper('sports', 'WSJ', 'wsj-sports')
	if toberun == 10:
	        run_twitter_newspaper('business', 'WSJ', 'wsj-ceo-council')
	if toberun == 11:
	        run_twitter_newspaper('entertainment', 'WSJ', 'fashion-week')
	if toberun == 12:
        	run_twitter_newspaper('technology', 'WSJ', 'wsj-tech')
	return


class getTwitterNewspaper(CronJobBase):

	RUN_EVERY_MINS = 1 # every 1 min

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'crsq.twitter_newspaper_run_twitter_newspaper_getTwitterNewspaper'    # a unique code

        def do(self):
                logger.debug("twitter_newspaper.run_twitter_newspaper - getTwitterNewspaper starts")
                time_dependent_tw_np(datetime.now().hour)
                return

