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

def get_super_categories(url):
	categories_list = []
	categories = page.Page(site, title=url.replace('/en/','')).getCategories()
	
	while categories!=None:
		categories_list.append(categories)
		print categories
		categories = map(lambda x: page.Page(site, title=x).getCategories(), categories)
		categories = sum(categories,[])

	return categories_list


#get_super_categories('/en/Sachin_Tendulkar')	

