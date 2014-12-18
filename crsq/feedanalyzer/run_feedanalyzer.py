from crsq.feedanalyzer import feedextractor
from crsq.models import ArticleInfo, TweetLinks, ArticleSemantics, ArticleTags
from datetime import datetime
import logging
from crsq.crsqlib.article_elastic_search import refreshdbtoes

from django_cron import CronJobBase, Schedule

logger = logging.getLogger(__name__)

def fa():
	logger.exception('run_feedanalyzer: Getting Feed Result')
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
	feedextractor.load_rss_in_table("http://rss1.smashingmagazine.com/feed/", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/labnol", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/Makeuseof", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/readwriteweb", "feed")
	feedextractor.load_rss_in_table("http://feeds.wired.com/GearFactor", "fromscratch")
	feedextractor.load_rss_in_table("http://www.ducttapemarketing.com/blog/feed/", "feed")
	feedextractor.load_rss_in_table("http://www.engadget.com/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.tmz.com/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.dailydot.com/feed/summary/latest/", "fromscratch")
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
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589699/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589702/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589704/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/647966/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589706/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589705/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589711/index.rss", "fromscratch")
        feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/647963/index.rss", "fromscratch")
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/home_page_top_stories.rss", "fromscratch")
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/market.rss", "fromscratch")
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/economy-policy-102.rss", "fromscratch")
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/finance-103.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://www.pakistantribune.com.pk/feed", "fromscratch")
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/management-107.rss", "fromscratch")
	feedextractor.load_rss_in_table("https://www.yahoo.com/tech/rss", "feed")
	countrylist = ["in", "us", "au", "uk", "en_sg"]
	topiclist = ["t", "s", "snc", "m", "w", "b", "ir", "h", "e", "p", "n"]
	for country in countrylist:
		for topic in topiclist:
			feedextractor.load_rss_in_table("https://news.google.com/news/feeds?ned=" + country + "&output=rss&topic="+topic, "fromscratch")
	feedextractor.load_rss_in_table("http://holykaw.alltop.com/feed", "fromscratch")
	nytlist = ["HomePage.xml", "AsiaPacific.xml", "Europe.xml", "MiddleEast.xml", "Africa.xml", "Americas.xml", "World.xml", "US.xml", "Politics.xml", "NYRegion.xml", "Business.xml", "EnergyEnvironment.xml", "MediaandAdvertising.xml", "Economy.xml", "Technology.xml", "PersonalTech.xml", "Health.xml", "Nutrition.xml", "Sports.xml", "Baseball.xml", "InternationalSports.xml", "Arts.xml", "ArtandDesign.xml", "Movies.xml", "Dance.xml", "Television.xml", "Music.xml", "FashionandStyle.xml", "DiningandWine.xml", "Travel.xml", "InternationalOpinion.xml"]
	feedextractor.load_rss_in_table("http://www.businessinsider.in/rss_section_feeds/2147477994.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://www.businessinsider.in/rss_section_feeds/21806366.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.nationalgeographic.com/ng/NGM/NGM_Magazine", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml?edition=int", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.bbci.co.uk/news/health/rss.xml?edition=int", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.bbci.co.uk/news/science_and_environment/rss.xml?edition=int", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.bbci.co.uk/news/rss.xml?edition=int", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.bbci.co.uk/news/world/europe/rss.xml?edition=int", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.bbci.co.uk/news/world/middle_east/rss.xml?edition=int", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.bbci.co.uk/news/world/asia/rss.xml?edition=int", "fromscratch")
	#for ny in nytlist:
		#feedextractor.load_rss_in_table("http://rss.nytimes.com/services/xml/rss/nyt/"+ny, "fromscratch") 
	#logger.exception('run_feedanalyzer: ' + ' articleinfo ' + str(ArticleInfo.objects.all().count()) + ' articlesemantics ' + str(ArticleSemantics.objects.all().count()) + ' articletags ' + str(ArticleTags.objects.values('url').distinct().count()))
	logger.exception("Load RSS in Table Done")
	refreshdbtoes()
	logger.exception("Refresh DB to ES Done")
	return

class getFeedAnalyzer(CronJobBase):

	RUN_EVERY_MINS = 1 # every 1 min
	
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'crsq.feedanalyzer_run_feedanalyzer_getFeedAnalyzer'    # a unique code

	def do(self):
		logger.debug("feedanalyzer.run_feedanalyzer - getFeedAnalyzer starts")
		fa()
		logger.exception("cron job getFeedAnalyzer done")
		return

