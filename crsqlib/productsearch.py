from amazon.api import AmazonAPI
import pickledb

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def getAmazonProducts(keywords, index):

	amazonproddb = pickledb.load('amazonprod.db', False)

        secret_key = '1U8FN957RXcYjF+3nRBUSrt7GFo5qOikY7r2sKYC'
        access_key = 'AKIAJN7RCVYN23USSAYQ'
        associate_tag = 'cb02-20'

        amazon = AmazonAPI(access_key, secret_key, associate_tag)
        output = []

        for kw in keywords:
		if amazonproddb.get(kw+index) == None:
	                try:
        	                response = amazon.search_n(1, Keywords=removeNonAscii(kw), SearchIndex=index)
				product = response[0]
				link = "http://www.amazon.com/dp/"+("000000"+str(product.asin)+"/")[-11:-1]+"?tag=cb02-20"
	                        output.append({'keyword': kw, 'link': link})
				amazonproddb.set(kw+index, link)
				amazonproddb.dump()
        	        except Exception as e:
                	        print 'Amazon Products Error: ' + str(e)
                        	raise
		else:
			output.append({'keyword': kw, 'link': amazonproddb.get(kw+index)})
        return output


