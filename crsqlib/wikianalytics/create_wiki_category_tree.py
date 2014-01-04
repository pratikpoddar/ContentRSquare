from crsqlib.wikianalytics import wikiutils
import pickledb

category_tree_db = pickledb.load('category_tree.db', False)
category_expanded_db = pickledb.load('category_expanded.db', False)

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def createCategoryTree(cat_id):

	if not category_expanded_db.get(cat_id) == None:
		print str(cat_id) + " already expanded"
		return

	categories = category_tree_db.get(cat_id)
	if categories == None:
		categories = wikiutils.getSubCategories(cat_id)
		category_tree_db.set(cat_id, categories)
		category_tree_db.dump()
		print str(cat_id) + " added"

	else:
		print str(cat_id) + " already added"

	for category in categories:
		try:
			createCategoryTree(category)
		except:	
			pass

	category_expanded_db.set(cat_id, 1)
	category_expanded_db.dump()
	print str(cat_id) + " expanded"

	return

createCategoryTree('7345184')
