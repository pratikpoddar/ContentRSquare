from crsq.models import *
from crsq.crsqlib.article_elastic_search import *

urls = map(lambda x: x['url'], ArticleInfo.objects.all().values('url'))
for url in urls:
    indexurl(url)

topterms = gettopterms()
