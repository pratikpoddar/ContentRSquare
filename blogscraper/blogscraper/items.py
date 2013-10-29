# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BlogArticle(Item):
    title = Field()
    link = Field()
    text = Field()
    date_published = Field()
    author = Field()
    bloglink = Field()
    typeofblog = Field()


