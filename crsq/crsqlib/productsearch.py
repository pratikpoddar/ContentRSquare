from amazon.api import AmazonAPI
from crsq.models import AmazonProd
import logging
from crsq.crsqlib.stringutils import *

logger = logging.getLogger(__name__)

def getAmazonProducts(keywords, index):

        secret_key = '1U8FN957RXcYjF+3nRBUSrt7GFo5qOikY7r2sKYC'
        access_key = 'AKIAJN7RCVYN23USSAYQ'
        associate_tag = 'cb02-20'

        amazon = AmazonAPI(access_key, secret_key, associate_tag)
        output = []
	logger.debug('productsearch.py - getAmazonProducts - ' + str(keywords) + ' ' + index)
        for kw in keywords:
		amazonlink = AmazonProd.objects.filter(text=kw, index=index).values('amazonlink')
		if not amazonlink:
	                try:
        	                response = amazon.search_n(1, Keywords=removeNonAscii(kw), SearchIndex=index)
                                if response:
    					product = response[0]
					link = "http://www.amazon.com/dp/"+("000000"+str(product.asin)+"/")[-11:-1]+"?tag=cb02-20"
				else:
					link = ''
	       	                output.append({'keyword': kw, 'link': link})
				try:
					amazonprod = AmazonProd()
					amazonprod.text = kw
					amazonprod.index = index
					amazonprod.amazonlink = link
					amazonprod.save()
				except Exception as e:
					logger.exception('productsearch.py - getAmazonProducts - Error in saving to AmazonProd ' + str(e))
					raise
        	        except Exception as e:
                	        logger.exception('productsearch.py - getAmazonProducts - Error: ' + str(e))
                        	raise
		else:
			output.append({'keyword': kw, 'link': amazonlink[0]['amazonlink']})
        return output


