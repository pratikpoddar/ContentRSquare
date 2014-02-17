from django.template.defaultfilters import slugify
from crsq.models import ArticleInfo, ArticleSemantics, ArticleTags
from urlparse import urlparse
import json
from crsq.crsqlib import urlutils, articleutils
import logging
from datetime import datetime, timedelta
from crsq.crsqlib.articleutilsdb import put_article_details, put_article_semantics_tags

logger = logging.getLogger(__name__)

def create_linkbook(urllist):

	for url in urllist:
		put_article_details(url)
		put_article_semantics_tags(url)
	return

urllist1 = ["http://blogs.hbr.org/2012/10/digital-staffing-the-future-of/", "http://www.forbes.com/sites/georgeanders/2013/04/10/who-should-you-hire-linkedin-says-try-our-algorithm/", "http://www.nytimes.com/2013/04/28/technology/how-big-data-is-playing-recruiter-for-specialized-workers.html", "http://knowledge.wharton.upenn.edu/article/mind-your-social-presence-big-data-recruiting-has-arrived/", "http://www.nytimes.com/2007/01/03/technology/03google.html", "http://www.hackdiary.com/2010/02/10/algorithmic-recruitment-with-github/", "http://proofcommunication.com/proof-to-help-zlemma-the-latest-in-stem-talent-identification/1251"]
ArticleInfo.objects.filter(url__in=urllist1).delete()
create_linkbook(urllist1)

l = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
print filter(lambda x: x not in l, urllist1)







	
	
	
