from wikitools import wiki
from wikitools import api
from wikitools import page

site = wiki.Wiki("http://en.wikipedia.org/w/api.php") 

def getSubCategories(category_id):
	params = {'action':'query', 'list':'categorymembers', 'cmpageid':category_id, 'cmtype':'subcat', 'cmlimit':'max'}
	request = api.APIRequest(site, params)

	result = []
	try:
		result += map(lambda x: str(x['pageid']), request.query().values()[0]['categorymembers'])
	except:
		pass

        try:
                result += map(lambda x: str(x['pageid']), request.query().values()[1]['categorymembers'])
        except:
                pass

	return result

def get_wiki_categories(url):
	return page.Page(site, title=url.replace('/en/','')).getCategories()
 

	

