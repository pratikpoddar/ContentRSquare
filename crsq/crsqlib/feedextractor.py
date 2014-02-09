import feedparser
from bs4 import BeautifulSoup
from crsq.models import ArticleInfo

rss_list = [ "http://feeds.feedburner.com/TechCrunch/" ]

entries = []
for rss_url in rss_list:
	feed = feedparser.parse(rss_url)
	entries.extend(feed['items'])
	

def put_article_details(entry):
        if ArticleInfo.objects.filter(url=url).count()==0:
                try:
			url = entry['feedburner_origlink']
			print url
                        socialpower = urlutils.getSocialShares(url)
                        articleinfo = ArticleInfo(url=url, articletitle = entry['title'], articleimage = entry['image'], articlecontent = BeautifulSoup(entry['content'][0]['value']).text, articledate = entry['published_parsed'], articlehtml = entry['content'][0]['value'], twitterpower= socialpower['tw'], fbpower = socialpower['fb'])
                        if len(articledict['cleaned_text'].strip())>1:
                                articleinfo.save()
                except Exception as e:
			print e
                        #logger.exception('twitter_newspaper - put_article_details - error saving article - ' + removeNonAscii(url) + ' - ' + str(e))
        return


sorted_entries = sorted(entries, key=lambda entry: entry['published_parsed'])
sorted_entries.reverse()
put_article_details(entries[0])



