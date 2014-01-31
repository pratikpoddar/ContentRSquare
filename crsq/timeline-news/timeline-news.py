from django.template.defaultfilters import slugify
from crsq.models import ArticleInfo, ArticleSemantics, ArticleTags
from urlparse import urlparse
import json
from crsq.crsqlib import urlutils, articleutils
import logging
from datetime import datetime, timedelta

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
		try:
			enddate = article['articledate']+ timedelta(days=1)
			json_object['endDate'] = str(enddate.year) + "," + str(enddate.month) + "," + str(enddate.day)
		except:
			pass
		json_object['headline'] = article['articletitle']
		json_object['text'] = articlesemantics['summary'][0:200] + " <a href='"+url+"' target='_blank'> .. more ..</a>"
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

def put_article_details(url):
        if ArticleInfo.objects.filter(url=url).count()==0:
                try:
                        articledict = articleutils.getArticlePropertiesFromUrl(url)
                        socialpower = urlutils.getSocialShares(url)
                        articleinfo = ArticleInfo(url=url, articletitle = articledict['title'], articleimage = articledict['image'], articlecontent = articledict['cleaned_text'], articledate = articledict['publish_date'], twitterpower= socialpower['tw'], fbpower = socialpower['fb'])
                        if len(articledict['cleaned_text'].strip())>1:
                                articleinfo.save()
                except Exception as e:
                        logger.exception('timeline_news - put_article_details - error saving article - ' + url + ' - ' + str(e))
        return

def put_article_semantics_tags(url):
        if ArticleInfo.objects.filter(url=url).count()==0:
                #logger.exception('twitter_newspaper - put_article_semantics_tags - error getting article content - ' + url + ' - ' + 'No content in ArticleInfo')
                return
        if ArticleSemantics.objects.filter(url=url).count()==0 or ArticleTags.objects.filter(url=url).count()==0:
                try:
                        content = ArticleInfo.objects.filter(url=url).values('articlecontent')[0]['articlecontent']
                        semantics_dict = articleutils.getArticleSemanticsTags(content)
                        semantics_row = ArticleSemantics(url=url, summary = semantics_dict['summary'], topic = semantics_dict['topic'])
                        if ArticleSemantics.objects.filter(url=url).count()==0:
                                semantics_row.save()
                        if ArticleTags.objects.filter(url=url).count()==0:
                                for tag in semantics_dict['tags']:
                                        tag_row = ArticleTags(url=url, tag=tag)
                                        if ArticleTags.objects.filter(url=url, tag=tag).count()==0:
                                                tag_row.save()
                except Exception as e:
                        logger.exception('timeline_news - put_article_semantics_tags - error getting article semantics / tags - ' + url + ' - ' + str(e))

        return

urllist = ["http://articles.economictimes.indiatimes.com/2014-01-14/news/46185342_1_fdi-arvind-kejriwal-delhi-polls", "http://indianexpress.com/article/india/politics/asserting-delhi-needs-jobs-arvind-kejriwal-scraps-nod-to-fdi-in-retail/", "http://www.financialexpress.com/news/cm-arvind-kejriwal-axes-sheila-dikshit-policy-rescinds-congress-approval-to-fdi-in-multibrand-retail-in-delhi/1218039/"]
ArticleInfo.objects.filter(url__in=urllist).delete()
create_timeline_json("Arvind Kejriwal in recent times", "Arvind Kejriwal is not the Chief Minister of Delhi and he has been acting a bit wierd lately. Some recent developments since he became CM" , urllist)







	
	
	
