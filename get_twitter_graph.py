import tweepy
import json
import jsonpickle
from time import sleep
import sys
from bulbs.neo4jserver import Graph, Config, NEO4J_URI

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
def removetick(s): return s.replace("'","")
def removementions(s): return ' '.join(i for i in s.split(' ') if not i.startswith('@'))
def removelinks(s): return ' '.join(i for i in s.split(' ') if not i.find('http') > -1)
def removelines(s): return s.replace("\n"," ")

def clean_status(s): return removelinks(removelines(removementions(removetick(removeNonAscii(s)))))

config = Config(NEO4J_URI)
g = Graph(config)

def getVertex(twitterid, minstage):
        vertices = g.vertices.index.lookup(twitterid=twitterid)
        if vertices:
                vertices = list(vertices)
                if len(vertices)!=1:
                        raise Exception("Assertion Error: getVertex: not a unique vertex with the same twitterid " + str(twitterid))
		vertex = vertices[0]
		if vertex.stage < minstage:
			raise Exception("Assertion Error: getVertex: vertex with stage value < " + str(minstage) + " - " + str(twitterid) + " " + str(vertex))
		return vertex
	else:
		raise Exception("Error: getVertex: No Vertex with twitterid " + str(twitterid))

def getStatus(twitterid):
	vertex = getVertex(twitterid, 2)
	print ""
	print "## getStatus " + str(twitterid) + ' ' + removeNonAscii(vertex.screen_name) + ' ' + removeNonAscii(vertex.name) + " ##"
	statuses = vertex.statuses
	statuses = json.loads(statuses)
	totalstatus = ""
	for status in statuses:
		if not status['in_reply_to_user_id_str']:
			totalstatus+=clean_status(status['text'])+" "
	return totalstatus

def getStatusStatistics(twitterid):
        vertex = getVertex(twitterid, 2)
        print ""
        print "## getStatusStatistics " + str(twitterid) + ' ' + removeNonAscii(vertex.screen_name) + ' ' + removeNonAscii(vertex.name) + " ##"
        statuses = vertex.statuses
        statuses = json.loads(statuses)
	mentions = []
	hashes = []
	favorite_count = 0
	retweet_count = 0
        for status in statuses:
		favorite_count += status['favorite_count']
		retweet_count += status['retweet_count']
		try:
			mentions += map(lambda x: x['id_str'], status['entities']['user_mentions'])
		except:
			pass
		try:
			hashes += map(lambda x: x['text'], status['entities']['hashtags'])
		except:
			pass
        return {'mentions': mentions, 'hashes': hashes, 'favorite_count': favorite_count, 'retweet_count': retweet_count}

## TODO: Implement it
def getFollowerStats(twitterid):
	vertex = getVertex(twitterid,3)
	print ""
        print "## getFollowerStats " + str(twitterid) + ' ' + removeNonAscii(vertex.screen_name) + ' ' + removeNonAscii(vertex.name) + " ##"
        followers = vertex.followers
	
	return {}
	
def printData(twitterid):
	try:
		vertex = getVertex(twitterid,0)
		print "----------------------"
		print removeNonAscii(str(vertex.twitterid)) + " - " + removeNonAscii(str(vertex.screen_name)) + " - " + removeNonAscii(str(vertex.name)) + " - " + removeNonAscii(str(vertex.location)) + " - " + removeNonAscii(str(vertex.description))
		print "Status Count: " + str(vertex.statuses_count) + " - Friends Count: " + str(vertex.friends_count) + " - Followers Count: " + str(vertex.followers_count) + " - Profiled: " + str(vertex.profiled) + " - StatusAnalyzed: " + str(vertex.status_analyzed)
		print "Alchemy Category: " + json.loads(str(vertex.alchemy_categories))['category']
		print "Alchemy Concepts: " + str(map(lambda x: x['text'], json.loads(str(vertex.alchemy_concepts))))
		print "Statuses:"
		print map(lambda x: clean_status(x['text']), json.loads(str(vertex.statuses)))
	except Exception as e:
		print "Exception " + str(e)
		pass
	return


