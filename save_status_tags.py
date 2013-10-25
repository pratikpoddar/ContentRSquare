import tweepy
import json
import jsonpickle
from time import sleep
import sys
from bulbs.neo4jserver import Graph, Config, NEO4J_URI
from status_summarize import get_Status_Concepts, get_Status_Categories, getStatus

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
def removetick(s): return s.replace("'","")
def removementions(s): return ' '.join(i for i in s.split(' ') if not i.startswith('@'))
def removelinks(s): return ' '.join(i for i in s.split(' ') if not i.startswith('http'))
def removelines(s): return s.replace("\n"," ")

def clean_status(s): return removelines(removelinks(removementions(removetick(removeNonAscii(s)))))

config = Config(NEO4J_URI)
g = Graph(config)

def save_Status_Tags(twitterid):
	gen = g.vertices.index.lookup(twitterid=twitterid)
	try:
		vertex = list(gen)[0]
	except:
		print str(twitterid) + " not in the database - taking 66690578"
		vertex = list(g.vertices.index.lookup(twitterid=66690578))[0]
	status = getStatus(twitterid)
	vertex.alchemy_concepts = jsonpickle.encode(get_Status_Concepts(status))
	vertex.alchemy_categories = jsonpickle.encode(get_Status_Categories(status))
	vertex.status_analyzed = 1
	vertex.save()

