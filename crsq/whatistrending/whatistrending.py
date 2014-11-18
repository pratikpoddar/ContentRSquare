from crsq.whatistrending import google_trends, search, twitter_trends, youtube_trends

def print_seperator():
    print ""
    for counter in range(0,4):
        print "----------------------------------"
    print ""

topic = 'cricket'

print_seperator()
print google_trends.get_all_google_trends()
print_seperator()
print twitter_trends.get_all_twitter_trends()
print_seperator()
print youtube_trends.get_all_youtube_trends()
print_seperator()
print search.get_quora_page(topic)
print_seperator()
print search.get_twitter_page(topic)
print_seperator()
print search.get_twitter_handles_from_topic(topic)
print_seperator()


