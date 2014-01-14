from crsq.twitter_newspaper import twitter_newspaper
from crsq.models import ArticleInfo, TweetLinks

def get_articles():
	tl = map(lambda x: x['url'], TweetLinks.objects.all().values('url'))
	ai = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
	tobeexpanded = list(set(tl)-set(ai))

	for l in tobeexpanded:
		twitter_newspaper.put_article_details(l)
	return

#twitter_newspaper.get_list_timeline('Technology', 'pratikpoddar', 'startups', 100)
#twitter_newspaper.get_list_timeline('Technology', 'dkhare', 'india-tech-and-vc', 100)
twitter_newspaper.get_list_timeline('Technology', 'Scobleizer', 'tech-news-people', 100)
twitter_newspaper.get_list_timeline('Entertainment', 'tellychakkar', 'celebs', 200)
get_articles()
