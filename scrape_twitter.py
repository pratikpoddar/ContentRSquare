import tweepy
import json
import jsonpickle
from time import sleep
import sys
import itertools

def checkRateLimit():
	
	ratelimit_list = api.rate_limit_status()['resources'].values()
	ratechoke = len(filter(lambda x: x['remaining']==0, reduce(lambda x,y: list(itertools.chain(x,y.values())), ratelimit_list, [])))
	if ratechoke > 0:
		print "Rate Limit Error. Please stop"
		sys.exit(0)
	return

def getProfiledList():
	profiledlist = []
	vertices = g.V
	for v in vertices:
		try:
			if v.profiled == 1:
				profiledlist.append(v.twitterid)
		except:
			pass
	print "Length of Profiled List: " + str(len(profiledlist))
	return profiledlist

def crsq_user_status_from_twitter(twitterid):
	try:
		page = 1
		statuslist = []
		while True:
			checkRateLimit()
			statuses = api.user_timeline(page=page, id=twitterid)
			if statuses:
				for status in statuses:
			            statuslist.append(status)
			else:
			        break
    			page += 1  # next page
			if page >= 4:
				break
		return statuslist
	except Exception as e:
		print "Restricted profile / Rate limit Exception / No Internet : " + str(twitterid) + " " + str(e)
		raise
	
def crsq_user_dict_from_twitter(twitterid):
	try:
		checkRateLimit()
		userObj = api.get_user(twitterid)
	except Exception as e:
		print "Restricted profile / Rate limit Exception / No Internet : " + str(twitterid) + " " + str(e)
		
		if str(e).find("Rate limit")>-1:
			sys.exit(1)
		if str(e).find("Failed to send request")>-1:
			sys.exit(1)

                returndict = dict(twitterid=twitterid, screen_name='', name='', statuses=jsonpickle.encode([]), statuses_count=0, location='', followers=jsonpickle.encode([]), followers_count=0, friends_count=0, description='')
		return returndict

	try:
		checkRateLimit()
		returndict = dict(twitterid=userObj.id, screen_name=userObj.screen_name, name=userObj.name, statuses=jsonpickle.encode(crsq_user_status_from_twitter(twitterid)), statuses_count=userObj.statuses_count, location=userObj.location, followers=jsonpickle.encode(userObj.followers_ids()), followers_count=userObj.followers_count, friends_count=userObj.friends_count, description=userObj.description)
		return returndict
	except Exception as e:	
		print "Restricted profile / Rate limit Exception / No Internet : " + str(userObj.id) + " " + str(userObj.screen_name) + " " + str(e)

		if str(e).find("Rate limit")>-1:
			sys.exit(1)
		if str(e).find("Failed to send request")>-1:
			sys.exit(1)

		returndict = dict(twitterid=userObj.id, screen_name=userObj.screen_name, name=userObj.name, statuses=jsonpickle.encode([]), statuses_count=userObj.statuses_count, location=userObj.location, followers=jsonpickle.encode([]), followers_count=userObj.followers_count, friends_count=userObj.friends_count, description=userObj.description)
		return returndict

	return

def expandVertex(vertex):
	followers = jsonpickle.decode(vertex.followers)
	followers = filter(lambda x: x not in profiledlist, followers)
	for follower in followers:
		vertex2 = createVertex(follower)
		createEdge(vertex, vertex2, "followed by")
	print "Expanded Vertex " + str(vertex.twitterid) + " " + str(vertex.screen_name)
	vertex.expanded = 1
	vertex.save()
	return
	
def createVertex(twitterid):
	vertex = check_if_profile_exists(twitterid)
	if not(vertex==None):
		print "Already there user " + str(vertex.twitterid) + " " + str(vertex.screen_name)
		return vertex
	else:
		crsquserDict = crsq_user_dict_from_twitter(twitterid)
		vertex = g.vertices.create(twitterid=crsquserDict['twitterid'])
		vertex.screen_name = crsquserDict['screen_name']
		vertex.name = crsquserDict['name']
		vertex.statuses = crsquserDict['statuses']
		vertex.statuses_count = crsquserDict['statuses_count']
		vertex.location = crsquserDict['location']
		vertex.followers = crsquserDict['followers']
		vertex.followers_count = crsquserDict['followers_count']
		vertex.friends_count = crsquserDict['friends_count']
		vertex.description = crsquserDict['description']
		vertex.profiled = 1
		vertex.save()
		print "Creating new user " + str(crsquserDict['twitterid']) + " " + str(crsquserDict['screen_name'])
	
	return vertex

def check_if_profile_exists(twitterid):
	vertices = g.vertices.index.lookup(twitterid=twitterid)
	if vertices:
                vertex = list(vertices)[0]
                print "--- Already there user " + str(twitterid)
                try:
			if vertex.profiled==1:
                                return vertex
			else:
				raise
			
                except:
                        print "--- User was there but no data: " + str(twitterid)
			print "--- Deleting user"
			g.vertices.delete(vertex.eid)
                        return None
	else:
		return None

def createEdge(vertex1, vertex2, string):
	vertices = g.vertices.index.lookup(twitterid=vertex1.twitterid)
	if vertices:
		vertex = list(vertices)[0]
		edges = vertex.outE(string)
		if edges:
			edgeslist = list(edges)
			for edge in edgeslist:
				if edge.inV().twitterid == vertex2.twitterid:
					print "Old edge " + str(vertex1.twitterid) + " " + str(vertex1.screen_name) + " connecting to " + str(vertex2.twitterid) + " " + str(vertex2.screen_name) + " via " + string

					return

	edge = 	g.edges.create(vertex1, string, vertex2)
	print str(vertex1.twitterid) + " connecting to " + str(vertex2.twitterid) + " via " + string

	return
		
## tweepy

consumer_key="nNRGguiHtC5AouxzUlZQ"
consumer_secret="T3df1h6SIqitUs50mlPlbrTN9JrEMZzZK9h6ChYCGw"
access_token="66690578-TeOd1CQGR6KaF3cQvyNE59XPLYLJ7HAmu2DLLqTri"
access_token_secret="rGJYuYUJiSnUEqP0wxDNpfNVidPxZFqkuKkGDu3i3jI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

## neo4j

from bulbs.neo4jserver import Graph, Config, NEO4J_URI
config = Config(NEO4J_URI)
g = Graph(config)
profiledlist = getProfiledList()

if __name__ == "__main__":
	#pratikpoddar
	v = createVertex(66690578)
	#anandlunia
	#v = createVertex(62438757)

	expandVertex(v)


