from bulbs.neo4jserver import Graph, Config, NEO4J_URI
config = Config(NEO4J_URI)
g = Graph(config)
print "Wiki Graph Connected"
try:
	print "Number of Nodes in the Graph: " + str(len(g.V))
except:
	pass

try:
	print "Number of Edges in the Graph: " + str(len(g.E))
except:
	pass

def get_or_create_node(url, crsqid):
	v = g.vertices.index.lookup(crsqid=crsqid)
	if v==None:
		v = g.vertices.create(crsqid=crsqid)
		print url + " created"
	v.url = url
	v.save()
	return v

def get_node_by_id(crsqid):
	v = g.vertices.index.lookup(crsqid=crsqid)
	if v == None:
		print crsqid
		return None
	else:
		return v
		
def get_or_create_edge(id1, id2):
	v1 = get_node_by_id(crsqid = id1)
	v2 = get_node_by_id(crsqid = id2)

	edges = v1.outE("links")
        if edges:
                for edge in list(edges):
                        if edge.inV().crsqid == id2:
                                return edge

	print str(id1) + " links " + str(id2)
	edge = g.edges.create(v1, "links", v2)
	return edge


