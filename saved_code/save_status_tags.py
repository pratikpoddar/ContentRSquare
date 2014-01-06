import tweepy
import json
import jsonpickle
from time import sleep
import sys
from bulbs.neo4jserver import Graph, Config, NEO4J_URI
from text_summarize import get_Text_Concepts, get_Text_Categories, get_Content_Analysis, get_Calais_Topics, get_Freebase_Meaning
from get_twitter_graph import getStatus, getStatusStatistics, getVertex, getFollowerStats
from scrape_twitter import profiledlistAnalyzed

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
def removetick(s): return s.replace("'","")
def removementions(s): return ' '.join(i for i in s.split(' ') if not i.startswith('@'))
def removelinks(s): return ' '.join(i for i in s.split(' ') if not i.startswith('http'))
def removelines(s): return s.replace("\n"," ")

def clean_status(s): return removelines(removelinks(removementions(removetick(removeNonAscii(s)))))

config = Config(NEO4J_URI)
g = Graph(config)

def save_Stats_Tags(twitterid):
	print "Trying to save Stats and Tags for : " + str(twitterid)
	if twitterid in profiledlistAnalyzed:
		print "Already Analyzed for twitterid " + str(twitterid)
		return
	vertex = getVertex(twitterid, 3)
	status = getStatus(vertex.twitterid)
	try:
		vertex.alchemy_concepts = jsonpickle.encode(get_Text_Concepts(status))
		vertex.alchemy_categories = jsonpickle.encode(get_Text_Categories(status))
		vertex.y_entities_categories = jsonpickle.encode(get_Content_Analysis(status))
		vertex.calaistopics = jsonpickle.encode(get_Calais_Topics(status))
		vertex.status_stats = jsonpickle.encode(getStatusStatistics(twitterid))
		vertex.follower_stats = jsonpickle.encode(getFollowerStats(twitterid))
		if vertex.alchemy_concepts != None:
			if vertex.alchemy_categories != None:
				if vertex.y_entities_categories != None:
					if vertex.calaistopics != None:
						if vertex.status_stats != None:
							if vertex.follower_stats != None:
								vertex.stage = 4

		vertex.save()

	except Exception as e:
		print "Exception in save_Stats_Tags : " + str(twitterid) + " " + str(e)
		raise

	return

if __name__ == "__main__":
	#pratikpoddar
        save_Stats_Tags(66690578)
        #anandlunia
        save_Stats_Tags(62438757)


	

