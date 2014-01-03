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

def handleTwitterApiException(twitterid, e):

	print "Restricted profile / Rate limit Exception / No Internet : " + str(twitterid) + " " + str(e)
	if str(e).find("Rate limit")>-1:
		sys.exit(1)
	if str(e).find("Failed to send request")>-1:
		sys.exit(1)

	return
	
def getProfiledList(level):
	profiledlist = []
	vertices = g.V
	for v in vertices:
		try:
			if level=='basic':
				if v.stage >= 1:
					profiledlist.append(v.twitterid)
			if level=='statusfollowers':
				if v.stage >= 2:
					profiledlist.append(v.twitterid)
			if level=='expanded':
				if v.stage >= 3:
					profiledlist.append(v.twitterid)
			if level=='analyzed':
				if v.stage >= 4:
					profiledlist.append(v.twitterid)
		except:
			pass
	print "Length of Profiled List: (" + level + ") " + str(len(profiledlist))
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
		handleTwitterApiException(twitterid, e)
		raise
	
def crsq_user_dict_from_twitter(twitterid, list_of_attr):
	try:
		checkRateLimit()
		userObj = api.get_user(twitterid)
		try:
			if 'statuses' in list_of_attr:
				checkRateLimit()
				statuses=jsonpickle.encode(crsq_user_status_from_twitter(twitterid))
			else:
				statuses=jsonpickle.encode([])
		except:
			handleTwitterApiException(twitterid, e)
			statuses=jsonpickle.encode([])
		
		try:
			if 'followers' in list_of_attr:
				checkRateLimit()
				followers=jsonpickle.encode(userObj.followers_ids())
			else:
				followers=jsonpickle.encode([])
		except:
			handleTwitterApiException(twitterid, e)
			followers=jsonpickle.encode([])
	
		returndict = dict(twitterid=userObj.id, screen_name=userObj.screen_name, name=userObj.name, statuses=statuses, statuses_count=userObj.statuses_count, location=userObj.location, followers=followers, followers_count=userObj.followers_count, friends_count=userObj.friends_count, description=userObj.description)
	
	except Exception as e:
		handleTwitterApiException(twitterid, e)
		sys.exit(1)

	return returndict

def getFollowersFromEdges(vertex):
	edges = vertex.outE("followed by")
	list_of_twitterids = []
	if edges:
		for edge in list(edges):
			list_of_twitterids.append(edge.inV().twitterid)
	return list_of_twitterids

def expandVertex(vertex):
	followers = jsonpickle.decode(vertex.followers)
	not_yet_edged = list(set(followers) - set(getFollowersFromEdges(vertex)))
	not_yet_profiled= filter(lambda x: x not in profiledlistBasic, followers)
	for follower in (not_yet_profiled+not_yet_edged):
		vertex2 = createVertex(follower, basicData)
		createEdge(vertex, vertex2, "followed by")
	print "Expanded Vertex " + str(vertex.twitterid) + " " + str(vertex.screen_name)
	if vertex.stage > 3:
		vertex.stage = vertex.stage
	else:
		vertex.stage = 3
	vertex.save()
	return

def createVertex(twitterid, list_of_attrs):
	vertex = getorcreateVertex(twitterid)
	if twitterid in profiledlistStatusFollowers:
		print str(vertex.twitterid) + " " + str(vertex.screen_name) + " already there"
		return vertex
	if (twitterid in profiledlistBasic) and not('statuses' in list_of_attrs) and not('followers' in list_of_attrs):
		print str(vertex.twitterid) + " " + str(vertex.screen_name) + " already there"
		return vertex
	crsquserDict = crsq_user_dict_from_twitter(twitterid, list_of_attrs)
	for attr in list_of_attrs:
		vertex.data()[attr] = crsquserDict[attr]
	if ('statuses' in list_of_attrs) and ('followers' in list_of_attrs):
		vertex.stage = 2 #detail-profiled
	else:
		vertex.stage = 1 #profiled
	vertex.save()

	print str(vertex.twitterid) + " " + str(vertex.screen_name) + " created - with attrs " + str(list_of_attrs)

	return vertex

def getorcreateVertex(twitterid):
	minstage = 1
        vertices = g.vertices.index.lookup(twitterid=twitterid)
        if vertices:
                vertices = list(vertices)
                if len(vertices)!=1:
                        raise Exception("Assertion Error: getorcreateVertex: not a unique vertex with the same twitterid " + str(twitterid))

                vertex = vertices[0]
                if vertex.stage < minstage:
                	raise Exception("Assertion Error: getorcreateVertex: vertex with stage value < " + str(minstage) + " - " + str(twitterid) + " " + str(vertex))
	        return vertex
	else:
                vertex = g.vertices.create(twitterid=twitterid)
                vertex.stage = 0
                vertex.save()
		return vertex

def createEdge(vertex1, vertex2, string):
	vertex1 = getorcreateVertex(vertex1.twitterid)
	vertex2 = getorcreateVertex(vertex2.twitterid)
	edges = vertex1.outE(string)
	if edges:
		for edge in list(edges):
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
profiledlistBasic = getProfiledList("basic")
profiledlistStatusFollowers = getProfiledList("statusfollowers")
profiledlistExpanded = getProfiledList("expanded")
profiledlistAnalyzed = getProfiledList("analyzed")

basicData = ['screen_name', 'name', 'statuses_count', 'location', 'followers_count', 'friends_count', 'description']

if __name__ == "__main__":
	#pratikpoddar
	v = createVertex(66690578, basicData + ['statuses', 'followers'])
	expandVertex(v)
	#anandlunia
	v = createVertex(62438757, basicData + ['statuses', 'followers'])


