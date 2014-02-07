from django.template.defaultfilters import slugify
from crsq.models import ArticleInfo, ArticleSemantics, ArticleTags
from urlparse import urlparse
import json
from crsq.crsqlib import urlutils, articleutils
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def create_linkbook(urllist):

	for url in urllist:
		put_article_details(url)
		put_article_semantics_tags(url)
	return

def put_article_details(url):
	url = urlutils.getCanonicalUrl(url)
        if ArticleInfo.objects.filter(url=url).count()==0:
                try:
                        articledict = articleutils.getArticlePropertiesFromUrl(url)
                        socialpower = urlutils.getSocialShares(url)
                        articleinfo = ArticleInfo(url=url, articletitle = articledict['title'], articleimage = articledict['image'], articlecontent = articledict['cleaned_text'], articledate = articledict['publish_date'], articlehtml = articledict['raw_html'], twitterpower= socialpower['tw'], fbpower = socialpower['fb'])
                        if len(articledict['cleaned_text'].strip())>1:
                                articleinfo.save()
                except Exception as e:
                        logger.exception('run_linkbook - put_article_details - error saving article - ' + url + ' - ' + str(e))
        return

def put_article_semantics_tags(url):
	url = urlutils.getCanonicalUrl(url)
        if ArticleInfo.objects.filter(url=url).count()==0:
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
                        logger.exception('run_linkbook - put_article_semantics_tags - error getting article semantics / tags - ' + url + ' - ' + str(e))

        return

urllist1 = ["http://blogs.hbr.org/2012/10/digital-staffing-the-future-of/", "http://www.forbes.com/sites/georgeanders/2013/04/10/who-should-you-hire-linkedin-says-try-our-algorithm/", "http://www.nytimes.com/2013/04/28/technology/how-big-data-is-playing-recruiter-for-specialized-workers.html", "http://knowledge.wharton.upenn.edu/article/mind-your-social-presence-big-data-recruiting-has-arrived/", "http://www.nytimes.com/2007/01/03/technology/03google.html", "http://www.hackdiary.com/2010/02/10/algorithmic-recruitment-with-github/", "http://proofcommunication.com/proof-to-help-zlemma-the-latest-in-stem-talent-identification/1251"]
ArticleInfo.objects.filter(url__in=urllist1).delete()
create_linkbook(urllist1)

l = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
print filter(lambda x: x not in l, urllist1)







	
	
	
