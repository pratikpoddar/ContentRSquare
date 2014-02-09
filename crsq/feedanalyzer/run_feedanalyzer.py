from crsq.feedanalyzer import feedextractor
from crsq.models import ArticleInfo, TweetLinks, ArticleSemantics, ArticleTags
from datetime import datetime
import logging

from django_cron import CronJobBase, Schedule

logger = logging.getLogger(__name__)

def fa():
	logger.debug('run_feedanalyzer - Getting Feed Result ')
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/startups")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/fundings-exits")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/social")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/Mobilecrunch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunchIT")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/gaming")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/crunchgear")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/Techcrunch/europe")
	logger.exception('run_feedanalyzer: ' + ' articleinfo ' + str(ArticleInfo.objects.all().count()) + ' articlesemantics ' + str(ArticleSemantics.objects.all().count()) + ' articletags ' + str(ArticleTags.objects.values('url').distinct().count()))
	return

class getFeedAnalyzer(CronJobBase):

	RUN_EVERY_MINS = 1 # every 1 min

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'crsq.feedanalyzer_run_feedanalyzer_getFeedAnalyzer'    # a unique code

        def do(self):
                logger.debug("feedanalyzer.run_feedanalyzer - getFeedAnalyzer starts")
                fa()
                return

