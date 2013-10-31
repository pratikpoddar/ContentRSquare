# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy.contrib.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from blogscraper.items import BlogArticle

import re

site = None

class BlogArticleSpider(CrawlSpider):
    name = "blogscraper"
    allowed_domains = ["cseblog.com"]
    start_urls = [
        "http://www.cseblog.com/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(deny=()), callback='parse_item', follow=True),
    )
    
    def parse_item(self, response):
        return parser(response)

def parser(response):
	if re.search("/\d+/\d+/.html", response.url):
		site = BeautifulSoup(response.body_as_unicode())
		items = []
		item = BlogArticle()
		item['title'] = site.find("h3" , {"class": "post-title" } ).text.strip()
		item['link'] = site.find("h3" , {"class": "post-title" } ).a.attrs['href']
		item['text'] = site.find("div" , {"class": "post-body" } )
		item['bloglink'] = 'http://www.cseblog.com'
		item['typeofblog'] = 'blogger'
		items.append(item)

		return items
	else:
		return []

