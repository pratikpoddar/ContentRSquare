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
	#logger.exception('run_feedanalyzer - Techcrunch starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/startups", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/fundings-exits", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/social", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/Mobilecrunch", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunchIT", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/TechCrunch/gaming", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/crunchgear", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/Techcrunch/europe", "feed")
        #logger.exception('run_feedanalyzer - Mashable/SmashingMag/Labnol/Makeuseof/RWW starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://feeds.mashable.com/Mashable", "feed")
	feedextractor.load_rss_in_table("http://rss1.smashingmagazine.com/feed/", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/labnol", "feed")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/Makeuseof", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/readwriteweb", "feed")
        #logger.exception('run_feedanalyzer - GearFactor/DTM/Endadget/TMZ/Dailydot/FastCompany/Huff starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://feeds.wired.com/GearFactor", "fromscratch")
	feedextractor.load_rss_in_table("http://www.ducttapemarketing.com/blog/feed/", "feed")
	feedextractor.load_rss_in_table("http://www.engadget.com/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.tmz.com/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.dailydot.com/feed/summary/latest/", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/fastcompany", "feed")
	feedextractor.load_rss_in_table("http://feeds.huffingtonpost.com/huffingtonpost/raw_feed", "feed")
        refreshdbtoes()
	#logger.exception('run_feedanalyzer - TOI starts - ' + str(ArticleInfo.objects.all().count()))
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
        refreshdbtoes()
	#logger.exception('run_feedanalyzer - ET starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://economictimes.indiatimes.com/rssfeedsdefault.cms", "fromscratch")
        feedextractor.load_rss_in_table("http://blogs.economictimes.indiatimes.com/main/feed/entries/rss", "fromscratch")
        feedextractor.load_rss_in_table("http://economictimes.indiatimes.com/rssfeeds/1373380680.cms", "fromscratch")
        feedextractor.load_rss_in_table("http://economictimes.indiatimes.com/Infotech/rssfeeds/13357270.cms", "fromscratch")
        feedextractor.load_rss_in_table("http://economictimes.indiatimes.com/rssfeeds/837555174.cms", "fromscratch")
        feedextractor.load_rss_in_table("http://economictimes.indiatimes.com/rssfeedstopstories.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://economictimendiatimes.com/News/rssfeeds/1715249553.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://economictimes.indiatimes.com/Markets/markets/rssfeeds/1977021501.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://economictimes.indiatimes.com/Infotech/rssfeeds/13357270.cms", "fromscratch")
        #logger.exception('run_feedanalyzer - Ecnonomist starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://www.economist.com/topics/chinese-economy/index.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.economist.com/topics/banking/index.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.economist.com/sections/economics/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.economist.com/sections/business-finance/rss.xml", "fromscratch")
        refreshdbtoes()
	#logger.exception('run_feedanalyzer - IndiaToday starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589699/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589702/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589704/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/647966/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589706/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589705/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/589711/index.rss", "fromscratch")
        feedextractor.load_rss_in_table("http://indiatoday.feedsportal.com/c/33614/f/647963/index.rss", "fromscratch")
        #logger.exception('run_feedanalyzer - Business Standard starts - ' + str(ArticleInfo.objects.all().count()))
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/home_page_top_stories.rss", "fromscratch")
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/market.rss", "fromscratch")
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/economy-policy-102.rss", "fromscratch")
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/finance-103.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://www.pakistantribune.com.pk/feed", "fromscratch")
        feedextractor.load_rss_in_table("http://www.business-standard.com/rss/management-107.rss", "fromscratch")
        refreshdbtoes()
	#logger.exception('run_feedanalyzer - DB/NakedCap/ZH/MR/ZDnet/Auto starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/dealbreaker", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/NakedCapitalism", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/zerohedge/feed", "fromscratch")
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/marginalrevolution/feed", "fromscratch")
	feedextractor.load_rss_in_table("http://www.zdnet.com/blog/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.zdnet.com/news/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.zdnet.com/topic/reviews/rss.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.motorlogy.com/feed/", "feed")
        feedextractor.load_rss_in_table("http://www.thetruthaboutcars.com/feed/rss/", "fromscratch")
        feedextractor.load_rss_in_table("http://feeds.feedburner.com/indianautosblog", "fromscratch")
        feedextractor.load_rss_in_table("http://www.autoblog.com/category/audi/rss.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://feeds2.feedburner.com/egmcartech", "fromscratch")
        #logger.exception('run_feedanalyzer - Gizmodo/Returns/Drive/Gizbot starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://www.gizmodo.in/rss_section_feeds/2147477989.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://www.gizmodo.in/rss_section_feeds/19124836.cms", "fromscratch")
	feedextractor.load_rss_in_table("http://www.gizmodo.in/rss_section_feeds/19124827.cms", "fromscratch")
        feedextractor.load_rss_in_table("http://www.goodreturns.in/rss/money-business-news-fb.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.drivespark.com/rss/drivespark-four-wheelers-fb.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.drivespark.com/rss/drivespark-two-wheelers-fb.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.gizbot.com/rss/gizbot-fb.xml", "fromscratch")
        #logger.exception('run_feedanalyzer - Gulfnews starts - ' + str(ArticleInfo.objects.all().count()))
        feedextractor.load_rss_in_table("http://gulfnews.com/cmlink/1.734148", "fromscratch")
        feedextractor.load_rss_in_table("http://gulfnews.com/cmlink/1.446098", "fromscratch")
        feedextractor.load_rss_in_table("http://gulfnews.com/cmlink/1.446095", "fromscratch")
        feedextractor.load_rss_in_table("http://gulfnews.com/cmlink/1.446097", "fromscratch")
        #logger.exception('run_feedanalyzer - Yahoo starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("https://www.yahoo.com/tech/rss", "feed")
        refreshdbtoes()
	#logger.exception('run_feedanalyzer - Google starts - ' + str(ArticleInfo.objects.all().count()))
	countrylist = ["in", "us", "au", "uk", "en_sg"]
	#countrylist = ["in", "us", "au", "uk"]
	topiclist = ["t", "s", "snc", "m", "w", "b", "ir", "h", "e", "p", "n"]
        #topiclist = ["t", "s", "snc", "m", "w", "b", "ir", "h", "e"]
	for country in countrylist:
		for topic in topiclist:
			feedextractor.load_rss_in_table("https://news.google.com/news/feeds?ned=" + country + "&output=rss&topic="+topic, "fromscratch")
        #logger.exception('run_feedanalyzer - Holykaw starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://holykaw.alltop.com/feed", "fromscratch")
        #logger.exception('run_feedanalyzer - Business Insider/BBC/NG/NDTV/LiveMint starts - ' + str(ArticleInfo.objects.all().count()))
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
	feedextractor.load_rss_in_table("http://feeds.feedburner.com/NdtvNews-TopStories", "fromscratch")
        feedextractor.load_rss_in_table("http://feeds.feedburner.com/NDTV-Business", "fromscratch")
        feedextractor.load_rss_in_table("http://feeds.feedburner.com/ndtv/TqgX", "fromscratch")
        feedextractor.load_rss_in_table("http://feeds.feedburner.com/NDTV-Tech", "fromscratch")
        feedextractor.load_rss_in_table("http://www.livemint.com/rss/consumer", "fromscratch")
        feedextractor.load_rss_in_table("http://www.livemint.com/rss/money", "fromscratch")
        feedextractor.load_rss_in_table("http://www.livemint.com/rss/economy_politics", "fromscratch")
        feedextractor.load_rss_in_table("http://www.livemint.com/rss/industry", "fromscratch")
        refreshdbtoes()
	#logger.exception('run_feedanalyzer - NZHerald starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000003.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_001501119.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_001503711.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000018.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000002.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000001.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000007.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000466.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000006.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_001503650.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000005.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000004.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://rss.nzherald.co.nz/rss/xml/nzhrsscid_001503726.xml", "fromscratch")
	refreshdbtoes()
        #logger.exception('run_feedanalyzer - Singapore/Malaysia/Thailand starts - ' + str(ArticleInfo.objects.all().count()))
	feedextractor.load_rss_in_table("http://straitstimes.com.feedsportal.com/c/32792/f/640960/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://straitstimes.com.feedsportal.com/c/32792/f/640962/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://straitstimes.com.feedsportal.com/c/32792/f/640964/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://straitstimes.com.feedsportal.com/c/32792/f/640965/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://straitstimes.com.feedsportal.com/c/32792/f/640958/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://www.straitstimes.com/news/sport/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://straitstimes.com.feedsportal.com/c/32792/f/640961/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://www.channelnewsasia.com/starterkit/servlet/cna/rss/home.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.channelnewsasia.com/starterkit/servlet/cna/rss/asiapacific.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.channelnewsasia.com/starterkit/servlet/cna/rss/business.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.channelnewsasia.com/starterkit/servlet/cna/rss/singapore.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://asiaone.feedsportal.com/c/34151/f/618414/index.rss", "fromscratch")
	feedextractor.load_rss_in_table("http://business.asiaone.com/rss.xml", "fromscratch")
	feedextractor.load_rss_in_table("http://www.financialexpress.com/section/industry/insurance/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.financialexpress.com/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.financialexpress.com/section/economy/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.financialexpress.com/section/lifestyle/travel-tourism/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.financialexpress.com/section/personal-finance/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.financialexpress.com/print/advertising-marketing/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.financialexpress.com/print/corporate-markets/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.financialexpress.com/print/economy-print/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.financialexpress.com/print/front-page/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.financialexpress.com/print/personal-finance-print/feed/", "fromscratch")
        feedextractor.load_rss_in_table("http://www.indiainfoline.com/rss/latestnews.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.indiainfoline.com/rss/businessnews.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.indiainfoline.com/rss/sectorbanking.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.indiainfoline.com/rss/sectorpharma.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.indiainfoline.com/rss/sectorinsurance.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.indiainfoline.com/rss/sectorrealestate.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.indiainfoline.com/rss/mutualfund.xml", "fromscratch")
        feedextractor.load_rss_in_table("http://www.indiainfoline.com/rss/economy.xml", "fromscratch")
        #logger.exception('run_feedanalyzer - ends - ' + str(ArticleInfo.objects.all().count()))
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

