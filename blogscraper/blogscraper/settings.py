# Scrapy settings for blogscraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'blogscraper'

SPIDER_MODULES = ['blogscraper.spiders']
NEWSPIDER_MODULE = 'blogscraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'blogscraper (+http://www.yourdomain.com)'
