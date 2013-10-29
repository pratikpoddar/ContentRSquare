# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy.spider import BaseSpider
from bs4 import BeautifulSoup

from blogscraper.items import BlogArticle

site = None

class BlogArticleSpider(BaseSpider):
    name = "blogscraper"
    allowed_domains = ["cseblog.com"]
    start_urls = [
        "http://www.cseblog.com/",
    ]

    def parse(self, response):
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

