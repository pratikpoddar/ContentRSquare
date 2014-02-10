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
	feedextractor.load_rss_in_table("http://feeds.mashable.com/Mashable")
	feedextractor.load_rss_in_table("http://yourstory.com/feed/")
	#feedextractor.load_rss_in_table("http://online.wsj.com/xml/rss/3_7014.xml")
	#feedextractor.load_rss_in_table("http://online.wsj.com/xml/rss/3_7041.xml")
	#feedextractor.load_rss_in_table("http://online.wsj.com/xml/rss/3_7031.xml")
	#feedextractor.load_rss_in_table("http://online.wsj.com/xml/rss/3_7201.xml")
	#feedextractor.load_rss_in_table("http://online.wsj.com/xml/rss/3_7455.xml")
	#feedextractor.load_rss_in_table("http://online.wsj.com/xml/rss/3_7085.xml")
	#feedextractor.load_rss_in_table("http://blogs.wsj.com/chinarealtime/feed/")
	#feedextractor.load_rss_in_table("http://blogs.wsj.com/wealth-manager/feed/")
	#feedextractor.load_rss_in_table("http://blogs.wsj.com/indiarealtime/feed/")
	#feedextractor.load_rss_in_table("http://blogs.wsj.com/japanrealtime/feed/")
	#feedextractor.load_rss_in_table("http://blogs.wsj.com/marketbeat/feed/")
	#feedextractor.load_rss_in_table("http://blogs.wsj.com/emergingeurope/feed/")
	#feedextractor.load_rss_in_table("http://blogs.wsj.com/privateequity/feed/")
	#feedextractor.load_rss_in_table("http://feeds.wsjonline.com/wsj/economics/feed")
	#feedextractor.load_rss_in_table("http://blogs.wsj.com/tech-europe/feed/")
	#feedextractor.load_rss_in_table("http://blogs.wsj.com/venturecapital/feed/")
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

