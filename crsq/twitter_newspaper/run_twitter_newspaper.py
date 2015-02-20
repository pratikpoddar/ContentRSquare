from crsq.twitter_newspaper import twitter_newspaper
from crsq.models import ArticleInfo, TweetLinks, ArticleSemantics, ArticleTags, DeleteLinks
from datetime import datetime
import logging
from crsq.crsqlib.article_elastic_search import refreshdbtoes
from random import shuffle
from crsq.crsqlib.timeout import timeout

from django_cron import CronJobBase, Schedule

logger = logging.getLogger(__name__)

@timeout(300.0)
def get_articles():
	tl = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))[-1000:]
	ai = map(lambda x: x['url'], ArticleInfo.objects.filter(url__in=tl).values('url'))
	tobeexpanded = list(set(tl)-set(ai))
	tobedeleted = map(lambda x: x['url'], DeleteLinks.objects.filter(url__in=tobeexpanded).values('url'))
	TweetLinks.objects.filter(url__in=tobedeleted).delete()
	tobeexpanded = list(set(tobeexpanded)-set(tobedeleted))
	logger.exception(str(len(tobeexpanded)) + " articles left from tweetlinks to get article info")
	shuffle(tobeexpanded)

	for l in tobeexpanded:
		logger.debug("twitter newspaper - getting article_info " + l)
		if urlutils.is_url_an_article(l):
			twitter_newspaper.put_article_details(l, source = 'twitter_newspaper')
			## hack
			twitter_newspaper.put_article_semantics_tags(l)
			## hack
			if ArticleInfo.objects.filter(url=l).count()==0:
				if DeleteLinks.objects.filter(url=l).count()==0:
					dl = DeleteLinks(url=l, reason="Reason could not be figured out")
					dl.save()
				TweetLinks.objects.filter(url=l).delete()
		else:
			if DeleteLinks.objects.filter(url=l).count()==0:
				dl = DeleteLinks(url=l, reason="Not an article")
				dl.save()
			TweetLinks.objects.filter(url=l).delete()
	return

@timeout(300.0)
def get_article_semantics_tags():
	tl = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))[-500:]
	ase = map(lambda x: x['url'], ArticleSemantics.objects.filter(url__in=tl).values('url'))
	tobeexpanded = list(set(tl)-set(ase))

	logger.exception(str(len(tobeexpanded)) + " articles left from tweetlinks to get sematics tags")
	for l in tobeexpanded:
		logger.debug("twitter newspaper - getting article_semantics_tags " + l)
		twitter_newspaper.put_article_semantics_tags(l)
	return

def run_twitter_newspaper(tuser, tlist):
	logger.exception("Starting to run twitter newspaper")
	logger.debug('run_twitter_newspaper - Getting Twitter Newspaper Result ' + tuser + tlist)
	twitter_newspaper.get_list_timeline(tuser, tlist, 100)
	get_articles()
	logger.exception("Get articles done")
	get_article_semantics_tags()
	logger.exception("Get article semantics tags done")
	#logger.exception('run_twitter_newspaper: ' + tuser + ' ' + tlist + ' articleinfo ' + str(ArticleInfo.objects.all().count()) + ' articlesemantics ' + str(ArticleSemantics.objects.all().count()) + ' articletags ' + str(ArticleTags.objects.values('url').distinct().count()) + ' tweetlinks ' + str(TweetLinks.objects.values('url').distinct().count()))
	return

@timeout(600.0)
def time_dependent_tw_np(toberun):

	run_twitter_newspaper('pratikpoddar', 'crsq-influencers-1')
	logger.exception("Run Twitter Newspaper Done")
	refreshdbtoes()
	logger.exception("Refresh DB to ES Done")
	return
	
class getTwitterNewspaper(CronJobBase):

	RUN_EVERY_MINS = 1 # every 1 min

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'crsq.twitter_newspaper_run_twitter_newspaper_getTwitterNewspaper'    # a unique code

	def do(self):
		logger.debug("twitter_newspaper.run_twitter_newspaper - getTwitterNewspaper starts")
		time_dependent_tw_np(datetime.now().hour)
		logger.exception("cron job getTwitterNewspaper done")
		return


