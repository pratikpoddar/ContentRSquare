from django.template.defaultfilters import slugify
from crsq.models import ArticleInfo, ArticleSemantics, ArticleTags
from urlparse import urlparse
import json
from crsq.crsqlib import urlutils, articleutils
import logging
from datetime import datetime, timedelta
from crsq.crsqlib.articleutilsdb import put_article_details, put_article_semantics_tags
logger = logging.getLogger(__name__)

def get_article_json(url):

	try:
		article = ArticleInfo.objects.filter(url=url).values()[0]
		articlesemantics = ArticleSemantics.objects.filter(url=url).values()[0]
		json_object = {}
		try:
			json_object['startDate'] = str(article['articledate'].year) + "," + str(article['articledate'].month) + "," + str(article['articledate'].day)
		except:
			json_object['startDate'] = "2010,1,1"
		#try:
			#enddate = article['articledate']+ timedelta(days=1)
			#json_object['endDate'] = str(enddate.year) + "," + str(enddate.month) + "," + str(enddate.day)
		#except:
			#pass
		json_object['headline'] = article['articletitle']
		json_object['text'] = articlesemantics['summary'][0:360] + " <a href='/timeline-news/article/"+slugify(article['articletitle'])+"/"+str(article['id'])+"' target='_blank'> .. more ..</a>"
		json_object['asset'] = { "media": article['articleimage'], "credit": urlparse(url)[1], "caption":""}

		return json_object
	except:
		return None

def get_timeline_json(headline, text, urllist):
	
	output = {}
	output['timeline'] = {}
	output['timeline']['headline'] = headline
	output['timeline']['type'] = 'default'
	output['timeline']['text'] = text
	output['timeline']['asset'] = { "media":"", "credit": "using Pratik Poddar CRSQ", "caption": "" }
	output['timeline']['date'] = filter(lambda x: x, map(lambda x: get_article_json(x) , urllist))
	
	return output


def create_timeline_json(headline, text, urllist):

	for url in urllist:
		put_article_details(url)
		put_article_semantics_tags(url)
	d = get_timeline_json(headline, text, urllist)
	j = json.dumps(d, indent=4)
	f = open('crsq/static/crsq/data/timeline-news/'+slugify(headline)+'.json', 'w')
	print >> f, j
	f.close()
	return

urllist1 = ["http://articles.economictimes.indiatimes.com/2014-01-14/news/46185342_1_fdi-arvind-kejriwal-delhi-polls", "http://indianexpress.com/article/india/politics/asserting-delhi-needs-jobs-arvind-kejriwal-scraps-nod-to-fdi-in-retail/", "http://www.financialexpress.com/news/cm-arvind-kejriwal-axes-sheila-dikshit-policy-rescinds-congress-approval-to-fdi-in-multibrand-retail-in-delhi/1218039/"]
ArticleInfo.objects.filter(url__in=urllist1).delete()
create_timeline_json("Arvind Kejriwal in recent times", "Arvind Kejriwal is not the Chief Minister of Delhi and he has been acting a bit wierd lately. Some recent developments since he became CM" , urllist1)

urllist2 = ['http://www.cbsnews.com/news/46-million-snapchat-usernames-phone-numbers-reportedly-leaked/', 'http://www.huffingtonpost.com/2014/01/15/rand-paul-snapchat_n_4602818.html', 'http://techcrunch.com/2014/01/14/snapchat-privacy-zuckerberg/', 'http://news.cnet.com/8301-1023_3-57617139-93/snapchat-apologizes-for-jump-in-spam/', 'http://www.businessinsider.in/16-Year-Old-Says-He-Can-Hack-Snapchat-And-Get-Your-Phone-Number/articleshow/29620436.cms', 'http://www.adweek.com/news/technology/audi-and-onions-snapchat-super-bowl-goes-quick-laughs-155433', 'http://www.wired.com/opinion/2014/01/secret-snapchats-monetization-success-will-surprise/', 'http://www.nbcnews.com/technology/snapchat-rolls-out-fix-after-hack-apologizes-2D11890019', 'http://www.nbcnews.com/technology/snapchat-turns-down-facebooks-3-billion-cash-offer-report-2D11591431', 'http://www.nbcnews.com/technology/bloody-teen-fight-over-sexts-wont-help-snapchats-reputation-8C11167242', 'http://www.nbcnews.com/technology/chill-mom-snapchats-self-destructing-messages-are-about-silliness-not-6C10065698', 'http://www.bbc.co.uk/news/technology-25572661', 'http://blogs.wsj.com/digits/2013/11/13/snapchat-spurned-3-billion-acquisition-offer-from-facebook/', 'http://mashable.com/2014/01/06/snapchat-facebook-acquisition-2/',  'http://www.forbes.com/sites/quora/2013/11/14/should-snapchat-have-accepted-facebooks-3-billion-cash-buyout-offer/', 'http://venturebeat.com/2013/11/13/snapchat-turned-down-a-3b-acquisition-offer-from-facebook/', 'http://www.businessinsider.in/Heres-What-The-LA-Startup-Scene-Thinks-About-Snapchats-CEO-And-His-Decision-To-Turn-Down-Billions/articleshow/27148062.cms', 'http://www.digitaltrends.com/social-media/5-craziest-mind-boggling-things-facebooks-rejected-offer-buy-snapchat-3-billion/', 'http://www.forbes.com/sites/jjcolao/2013/10/25/is-snapchat-raising-another-round-at-a-3-5-billion-valuation/', 'http://techcrunch.com/2012/10/29/billion-snapchats/', 'http://www.forbes.com/sites/jjcolao/2012/11/27/snapchat-the-biggest-no-revenue-mobile-app-since-instagram/', 'http://allthingsd.com/20121029/fast-growing-photo-messaging-app-snapchat-launches-on-android/', 'http://techcrunch.com/2013/10/03/snapchat-gets-its-own-timeline-with-snapchat-stories-24-hour-photo-video-tales/', 'http://finance.fortune.cnn.com/2013/06/26/snapchats-liquidity-trap/', 'http://www.newstatesman.com/sci-tech/2013/07/snapchat-pivots-privacy-publicity', 'http://www.dailymail.co.uk/news/article-2285961/Snapchat-Frank-Reginald-Brown-suing-founders-photo-app-claims-stole-idea-him.html', 'http://techcrunch.com/2013/11/06/the-snapchat-co-founder-lawsuit-drama-drags-on/', 'http://www.businessinsider.in/Snapchat-Has-Twice-Tried-And-Failed-To-Settle-Its-Lawsuit-With-Ousted-Co-Founder-Reggie-Brown/articleshow/27609207.cms', 'http://finance.yahoo.com/blogs/breakout/snapchat-hack-may-have-just-cost-the-company-founder--4-billion-155733225.html', 'http://survata.com/blog/is-snapchat-only-used-for-sexting-we-asked-5000-people-to-find-out/', 'http://techcrunch.com/2012/12/26/inside-snapchat-the-little-photo-sharing-app-that-launched-a-sexting-scare/', 'http://www.forbes.com/sites/jjcolao/2013/06/24/snapchat-raises-60-million-from-ivp-at-800-million-valuation/']
ArticleInfo.objects.filter(url__in=urllist2).delete()
create_timeline_json("Story of SnapChat", "Its the app that everyone is talking about. It rejected facebook's multi billion dollar offer. Lets see its story", urllist2)

urllist3 =['http://www.businessinsider.in/Indias-Left-Leaning-Anti-Graft-Party-Made-A-Stunning-Debut/articleshow/27328073.cms', 'http://articles.economictimes.indiatimes.com/2013-05-19/news/39369935_1_aam-aadmi-party-workers-police-action', 'http://www.frontline.in/static/html/fl2925/stories/20121228292503200.htm', 'http://articles.timesofindia.indiatimes.com/2012-09-19/india/33951624_1_anna-hazare-team-anna-members-political-alternative', 'http://indiatoday.intoday.in/story/what-is-the-aam-aadmi-party-all-about/1/234564.html', 'http://www.bbc.co.uk/news/world-asia-india-20492056', 'http://indiatoday.intoday.in/story/arvind-kejriwal-names-his-political-party-as-aam-aadmi-party/1/234522.html', 'http://indiatoday.intoday.in/story/arvind-kejriwal-aam-aadmi-party-formal-launch-jantar-mantar/1/234729.html', 'http://www.thehindu.com/news/national/aam-aadmi-party-now-a-registered-political-party/article4539185.ece', 'http://www.aamaadmiparty.org/page/goal-of-swaraj', 'http://articles.economictimes.indiatimes.com/2013-09-27/news/42463933_1_evms-ballot-paper-election-commission', 'http://www.hindustantimes.com/India-news/NewDelhi/Shanti-Bhushan-donates-Rs-1-crore-to-Kejriwal-s-Aam-Aadmi-Party/Article1-964698.aspx', 'http://ibnlive.in.com/news/indianamericans-extend-support-to-kejriwals-aam-aadmi-party/392801-37.html', 'http://articles.timesofindia.indiatimes.com/2013-03-23/delhi/37959821_1_leader-arvind-kejriwal-today-fake-bills-inflated-bills', 'http://www.thehindu.com/news/cities/Delhi/civil-society-groups-support-kejriwals-campaign-against-inflated-power-bills/article4576216.ece', 'http://www.ndtv.com/article/india/will-work-at-sit-in-files-are-being-delivered-to-me-arvind-kejriwal-473239?pfrom=home-lateststories', 'http://www.ndtv.com/article/india/aap-leaders-shout-at-cops-allege-supporters-are-being-detained-beaten-up-473272?curl=1391240450', 'http://articles.economictimes.indiatimes.com/2014-01-21/news/46411239_1_arvind-kejriwal-aam-aadmi-party-aap-demands', 'http://www.ndtv.com/article/cities/arvind-kejriwal-calls-off-sit-in-that-gridlocked-delhi-shocked-centre-473818?pfrom=home-lateststories', 'http://ibnlive.in.com/news/aam-aadmi-party-gets-broom-as-election-symbol/410942-37.html', 'http://ibnlive.in.com/news/delhi-aap-promises-700-litres-of-free-water-cheap-power-jan-lokpal/435206-80-258.html', 'http://www.firstpost.com/politics/aap-picks-its-candidates-filmmaker-homemaker-and-loyalists-800919.html', 'http://zeenews.india.com/news/nation/aap-sting-operation-arvind-kejriwal-cries-conspiracy-shazia-ilmi-offers-to-resign_891586.html', 'http://indiatoday.intoday.in/story/ec-begins-inquiry-into-sting-operation-against-aap-leaders/1/326154.html', 'http://www.ndtv.com/article/india/fulfill-promises-sheila-dikshit-tells-aam-aadmi-party-462091?curl=1387819909', 'http://timesofindia.indiatimes.com/assembly-elections-2013/delhi-assembly-elections/Aam-Admi-Arvind-Kejriwal-takes-oath-as-Delhi-CM-vows-change-in-governance/articleshow/28047952.cms', 'http://archive.indianexpress.com/news/aap-gears-for-lok-sabha-polls-to-fight-300-seats/1215513/', 'http://articles.economictimes.indiatimes.com/2014-01-08/news/45991566_1_anjali-damania-aap-ticket-maharashtra', 'http://www.ndtv.com/article/cheat-sheet/one-month-of-arvind-kejriwal-s-government-five-hits-and-five-misses-476214', 'http://articles.economictimes.indiatimes.com/2014-01-09/news/46030260_1_prashant-bhushan-aap-aam-aadmi-party']
ArticleInfo.objects.filter(url__in=urllist3).delete()
create_timeline_json("Story of AAP", "The complete story of Aam Aadmi Party", urllist3)


l = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
print filter(lambda x: x not in l, urllist1+urllist2+urllist3)







	
	
	
