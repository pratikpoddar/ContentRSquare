from crsq.twitter_newspaper import twitter_newspaper
from crsq.models import ArticleInfo, TweetLinks, ArticleSemantics, ArticleTags
from datetime import datetime
import logging

from django_cron import CronJobBase, Schedule

logger = logging.getLogger(__name__)

def get_articles():
	tl = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))
	ai = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
	tobeexpanded = list(set(tl)-set(ai))

	for l in tobeexpanded:
		twitter_newspaper.put_article_details(l, source = 'twitter_newspaper')
	return

def get_article_semantics_tags():
	tl = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))
	as1 = map(lambda x: x['url'], ArticleSemantics.objects.all().values('url'))
	as2 = map(lambda x: x['url'], ArticleTags.objects.all().values('url'))
	tobeexpanded = list(set(list(set(tl)-set(as1)) + list(set(tl)-set(as2))))

	for l in tobeexpanded:
		twitter_newspaper.put_article_semantics_tags(l)
	return

def run_twitter_newspaper(tuser, tlist):
	logger.debug('run_twitter_newspaper - Getting Twitter Newspaper Result ' + tuser + tlist)
	twitter_newspaper.get_list_timeline(tuser, tlist, 40)
	get_articles()
	get_article_semantics_tags()
	logger.exception('run_twitter_newspaper: ' + tuser + ' ' + tlist + ' articleinfo ' + str(ArticleInfo.objects.all().count()) + ' articlesemantics ' + str(ArticleSemantics.objects.all().count()) + ' articletags ' + str(ArticleTags.objects.values('url').distinct().count()) + ' tweetlinks ' + str(TweetLinks.objects.values('url').distinct().count()))
	return

def time_dependent_tw_np(toberun):

	toberun = toberun % 15

	if toberun == 0:
		run_twitter_newspaper('pratikpoddar', 'startups')
	if toberun == 1:
		run_twitter_newspaper('dkhare', 'india-tech-and-vc')
	if toberun == 2:
		run_twitter_newspaper('Scobleizer', 'tech-news-people')
	if toberun == 3:
	        run_twitter_newspaper('mashable', 'startups-silicon-valley-24')
	if toberun == 4:
	        run_twitter_newspaper('mashable', 'startups-nyc-24')
	if toberun == 5:
	        run_twitter_newspaper('mashable', 'tech')
	if toberun == 6:
	        run_twitter_newspaper('mashable', 'music')
	if toberun == 7:
		run_twitter_newspaper('tellychakkar', 'celebs')
	if toberun == 8:
	        run_twitter_newspaper('WSJ', 'wsj-money')
	if toberun == 9:
	        run_twitter_newspaper('WSJ', 'wsj-sports')
	if toberun == 10:
	        run_twitter_newspaper('WSJ', 'wsj-ceo-council')
	if toberun == 11:
	        run_twitter_newspaper('WSJ', 'fashion-week')
	if toberun == 12:
        	run_twitter_newspaper('WSJ', 'wsj-tech')
	if toberun == 13:
		run_twitter_newspaper('theweek', 'politics')
	if toberun == 14:
		run_twitter_newspaper('mattklewis', 'political-journalists')
	return


class getTwitterNewspaper(CronJobBase):

	RUN_EVERY_MINS = 1 # every 1 min

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'crsq.twitter_newspaper_run_twitter_newspaper_getTwitterNewspaper'    # a unique code

        def do(self):
                logger.debug("twitter_newspaper.run_twitter_newspaper - getTwitterNewspaper starts")
                time_dependent_tw_np(datetime.now().hour)
                return

