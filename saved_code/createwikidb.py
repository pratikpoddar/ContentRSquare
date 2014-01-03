from wikidb import *

count = 1
with open('/home/gauri/Downloads/titles-sorted.txt') as f:
    for line in f:
        url = "http://en.wikipedia.org/wiki/" + line.strip()
	crsqid = count
	get_or_create_node(url, crsqid)
	count += 1

with open('/home/gauri/Downloads/links-simple-sorted.txt') as f:
    for line in f:
	list_of_id2 = map(lambda x: int(x), filter(lambda x: x, line.split(':')[1].split(' ')))
	id1 = int(line.split(':')[0])
	for id2 in list_of_id2:
		get_or_create_edge(id1, id2)
	
