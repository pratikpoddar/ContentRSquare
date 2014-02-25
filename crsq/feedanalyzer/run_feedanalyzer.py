from crsq.feedanalyzer import feedextractor
from crsq.models import ArticleInfo, TweetLinks, ArticleSemantics, ArticleTags
from datetime import datetime
import logging

from django_cron import CronJobBase, Schedule

logger = logging.getLogger(__name__)

def fa():
	logger.debug('run_feedanalyzer - Getting Feed Result ')
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/startups", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/fundings-exits", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/social", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/Mobilecrunch", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunchIT", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/gaming", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/crunchgear", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/Techcrunch/europe", "feed")
	feedextractor.load_rss_in_table("http://feeds.mashable.com/Mashable", "feed")
	feedextractor.load_rss_in_table("http://yourstory.com/feed/", "feed")
	feedextractor.load_rss_in_table("http://www.npr.org/rss/rss.php?id=1006", "feed")
	feedextractor.load_rss_in_table("http://www.npr.org/rss/rss.php?id=1004", "feed")
	feedextractor.load_rss_in_table("http://www.npr.org/rss/rss.php?id=1014", "feed")
	feedextractor.load_rss_in_table("http://www.npr.org/rss/rss.php?id=1008", "feed")
	feedextractor.load_rss_in_table("http://rss1.smashingmagazine.com/feed/", "feed")
	feedextractor.load_rss_in_table("http://feeds.wired.com/GearFactor", "fromscratch")
	feedextractor.load_rss_in_table("http://www.ducttapemarketing.com/blog/feed/", "feed")
	feedextractor.load_rss_in_table("http://www.engadget.com/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.tmz.com/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/fastcompany", "feed")
	feedextractor.load_rss_in_table("http://feeds.huffingtonpost.com/huffingtonpost/raw_feed", "feed")
	feedextractor.load_rss_in_table("http://timesofindia.feedsportal.com/c/33039/f/533965/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/296589292.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/1898055.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/7098551.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/5880659.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/1081479906.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/1081479906.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/2886704.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/784865811.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/2647163.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/3908999.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/-2128838597.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/-2128839596.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/-2128816011.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/2950623.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/30359486.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://timesofindia.indiatimes.com/rssfeeds/7098551.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://blogs.timesofindia.indiatimes.com/main/feed/entries/rss", "fromscratch")
	feedextractor.load_rss_in_table("http://blogs.economictimes.indiatimes.com/main/feed/entries/rss", "fromscratch")
	htlist = ["HT-Dontmiss", "HT-India", "HT-World", "HT-Entertainment", "HT-Bollywood", "HT-Fashion", "HT-Sexandrelationships", "HT-Wellness", "HT-ArtNews", "HT-Travel", "HT-Entertainment", "HT-Gadgets-updates", "HT-Apps-updates", "HT-Sport", "HT-cricket", "HT-Football", "HT-Business", "HT-Wellness", "HT-Mumbai-News", "HT-New-Delhi", "HT-Business"]
	for ht in htlist:
		feedextractor.load_rss_in_table("http://feeds.hindustantimes.com/"+ht, "fromscratch")
	countrylist = ["in", "us"]
	topiclist = ["t", "s", "snc", "m", "w", "b", "ir", "h", "e"]
	for country in countrylist:
		for topic in topiclist:
			feedextractor.load_rss_in_table("https://news.google.com/news/feeds?ned=" + country + "&output=rss&topic="+topic, "fromscratch")
	feedextractor.load_rss_in_table("http://holykaw.alltop.com/feed", "fromscratch")
	nytlist = ["HomePage.xml", "AsiaPacific.xml", "Europe.xml", "MiddleEast.xml", "Africa.xml", "Americas.xml", "World.xml", "US.xml", "Politics.xml", "NYRegion.xml", "Business.xml", "EnergyEnvironment.xml", "MediaandAdvertising.xml", "Economy.xml", "Technology.xml", "PersonalTech.xml", "Health.xml", "Nutrition.xml", "Sports.xml", "Baseball.xml", "InternationalSports.xml", "Arts.xml", "ArtandDesign.xml", "Movies.xml", "Dance.xml", "Television.xml", "Music.xml", "FashionandStyle.xml", "DiningandWine.xml", "Travel.xml", "InternationalOpinion.xml"]
	#for ny in nytlist:
		#feedextractor.load_rss_in_table("http://rss.nytimes.com/services/xml/rss/nyt/"+ny, "fromscratch") 
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

