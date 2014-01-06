from amazon.api import AmazonAPI
from functools32 import lru_cache

@lru_cache(maxsize=128)
def getAmazonProducts(keywords, index):

        secret_key = '1U8FN957RXcYjF+3nRBUSrt7GFo5qOikY7r2sKYC'
        access_key = 'AKIAJN7RCVYN23USSAYQ'
        associate_tag = 'cb02-20'

        amazon = AmazonAPI(access_key, secret_key, associate_tag)
        output = []

        for kw in keywords:
                try:
                        response = amazon.search_n(1, Keywords=kw, SearchIndex=index)
			product = response[0]
			link = "http://www.amazon.com/dp/"+("000000"+str(product.asin)+"/")[-11:-1]+"?tag=cb02-20"
                        output.append({'keyword': kw, 'link': link})
                except Exception as e:
                        print 'Amazon Products Error: ' + str(e)
                        pass

        return output


