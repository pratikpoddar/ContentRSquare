from crsq.crsqlib.text_summarize import text_summarize
from crsq.crsqlib import productsearch
from lxml import objectify
import bottlenose
import hashlib
import collections
import sys
import logging
import pickle
from crsq.crsqlib.stringutils import *

from crsq.models import ContentAffiliate

logger = logging.getLogger(__name__)

def convert(d):
    if isinstance(d, basestring):
        return str(d)
    elif isinstance(d, collections.Mapping):
        return dict(map(convert, d.iteritems()))
    elif isinstance(d, collections.Iterable):
        return type(d)(map(convert, d))
    else:
        return d

def content_affiliate(content, index):

	content = removeNonAscii(content)
	logger.debug('content_affiliate_advertising.py - content_affiliate - calls - ' + content[0:100]) 
	try:
		combined_hash = str(int(hashlib.md5(content.replace(' ','')+index.replace(' ','')).hexdigest(), 16))
		affiliate_result = ContentAffiliate.objects.filter(contenthash=str(combined_hash)).values('affiliate')
		if not affiliate_result:
			output = get_Content_Affliate_Advertising(content, index)
			try:
				content_affiliate = ContentAffiliate()
				content_affiliate.contenthash = str(combined_hash)
				content_affiliate.affiliate = pickle.dumps(output)
				content_affiliate.content = content[0:100]
				content_affiliate.save()
			except Exception as e:
				logger.exception('content_affiliate_advertising.py - content_affiliate - Error in saving in ContentAffiliate ' + str(e))
			logger.debug('content_affiliate_advertising.py - content_affiliate - returns - ' + str(output))
			return convert(output)

		else:
			logger.debug('content_affiliate_advertising.py - content_affiliate - returns - ' + str(pickle.loads(affiliate_result[0]['affiliate'])))
			return convert(pickle.loads(affiliate_result[0]['affiliate']))
	
	except Exception as e:
		logger.exception('content_affiliate_advertising.py - content_affiliate - error - ' + str(e))
		output = get_Content_Affliate_Advertising(content, index)
		logger.debug('content_affiliate_advertising.py - content_affiliate - returns - ' + str(output))
		return convert(output)

def get_Content_Affliate_Advertising(content, index):

	keywords = []

        try:
                keywords += map(lambda x: x['text'], text_summarize.get_topia_termextract(content))
        except Exception as e:
		logger.exception('content-affiliate-advertising.py - get_Content_Affiliate_Advertising - ' + str(e) + ' - get_topia_termextract')
                pass

	keywords = list(set(keywords))
	#keywords = ["Columbia Business School", "IBM"]

	products = []
	try:
		products = productsearch.getAmazonProducts(keywords, index)
	except Exception as e:
		logger.exception('content-affiliate-advertising.py - get_Content_Affiliate_Advertising - ' + str(e) + ' - get_Amazon_Products')
		pass
	return products

text = "Back in 2012 Id been to enough tech startup conferences in Europe over the previous few years to work out which ones appeared to be most significant. Europe being the disjointed bunch of countries that it is has too many to mention. That ended up being a post about events in 2013. Now, with 2014 already here, I figured plenty of readers would like an update. So here it is. A huge thanks to Heisenberg Media for helping me put this together. Thanks also to Conferize for their crowd-sourced list of European Tech Events in 2014 which you can find here. That is not our list, its theirs, but its pretty good. We also recommend the listing over at Lanyrd. But, simply being listed below does NOT imply that any of these events are endorsed by or partnered with TechCrunch, other than TechCrunch branded ones of course. This is a purely editorial list, based on our experience in Europe, the list is designed to help the European tech scene grow and get more organised. Simple. Why is it important to do this In the first instance, Europe is a bit of a mess. Every single country seems to have its own major conference on tech startups. And so we need a single overview of whats going on."

index = "Books"

#output = content_affiliate(text, index)
##print "[{'keyword':'Columbia Business School', 'link':'http://www.cseblog.com'}]"
#print output


