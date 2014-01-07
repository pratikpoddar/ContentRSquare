from crsqlib.wikianalytics import wikiutils
import pickledb

category_tree_db = pickledb.load('category_tree.db', False)
pendingqueue = ['7345184']

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def populateCategoryTree(cat_id):

	categories = category_tree_db.get(cat_id)
	if categories == None:
		categories = wikiutils.getSubCategories(cat_id)
		category_tree_db.set(cat_id, categories)
		category_tree_db.dump()
		pendingqueue.extend(categories)
		print str(cat_id) + " added"

	else:
		pendingqueue.extend(categories)
		print str(cat_id) + " already added"

	pendingqueue.remove(cat_id)
	return

def createCategoryTree():
	while pendingqueue:
		populateCategoryTree(pendingqueue[0])

createCategoryTree()

