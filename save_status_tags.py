import tweepy
import json
import jsonpickle
from time import sleep
import sys
from bulbs.neo4jserver import Graph, Config, NEO4J_URI
from status_summarize import get_Status_Concepts, get_Status_Categories, get_Content_Analysis, get_Calais_Topics, get_Freebase_Meaning
from get_twitter_graph import getStatus, getStatusStatistics

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
def removetick(s): return s.replace("'","")
def removementions(s): return ' '.join(i for i in s.split(' ') if not i.startswith('@'))
def removelinks(s): return ' '.join(i for i in s.split(' ') if not i.startswith('http'))
def removelines(s): return s.replace("\n"," ")

def clean_status(s): return removelines(removelinks(removementions(removetick(removeNonAscii(s)))))

config = Config(NEO4J_URI)
g = Graph(config)

def save_Status_Tags(twitterid):
	print "Trying to save Status Tags for : " + str(twitterid)
	gen = g.vertices.index.lookup(twitterid=twitterid)
	try:
		vertex = list(gen)[0]
	except:
		print str(twitterid) + " not in the database - taking 66690578"
		twitterid = 66690578
		vertex = list(g.vertices.index.lookup(twitterid=66690578))[0]
	status = getStatus(twitterid)
	try:
		vertex.alchemy_concepts = jsonpickle.encode(get_Status_Concepts(status))
		vertex.alchemy_categories = jsonpickle.encode(get_Status_Categories(status))
		vertex.y_entities_categories = jsonpickle.encode(get_Content_Analysis(status))
		vertex.calaistopics = jsonpickle.encode(get_Calais_Topics(status))
		vertex.status_stats = jsonpickle.encode(getStatusStatistics(twitterid))
		if vertex.alchemy_concepts != None:
			if vertex.alchemy_categories != None:
				if vertex.y_entities_categories != None:
					if vertex.calaistopics != None:
						if vertex.status_stats != None:
							vertex.status_analyzed = 2
		try:
			vertex.real_location = get_Freebase_Meaning(vertex.location)['wikilink']
		except:
			vertex.real_location = vertex.location
		vertex.save()
	except Exception as e:
		print "Exception in save_Status_Tags : " + str(twitterid) + " " + str(e)
		raise

	return

def get_Not_Status_Analyzed_People():
        not_stat_analy_list = []
        vertices = g.V
	
	for v in vertices:
		try:
			not_stat_analy_list.append(v.twitterid)
		except:
			pass

        for v in vertices:
                try:
                        if v.status_analyzed == 2:
                                not_stat_analy_list.remove(v.twitterid)
                except:
			pass
                        
        print "Length of Not Status Analyze List: " + str(len(not_stat_analy_list))
        return not_stat_analy_list


if __name__ == "__main__":
	not_stat_analy_list = get_Not_Status_Analyzed_People()
	if len(not_stat_analy_list)>0:
		save_Status_Tags(not_stat_analy_list[0])
	

