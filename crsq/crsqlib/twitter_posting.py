import tweepy

logger = logging.getLogger(__name__)

consumer_key="GvQlGiyFI3YwNtcYSfZkuxHLg"
consumer_secret="i1jmdb41hjqxRHmXfncjcoY5ijq03Ha8Vd6XB2fpFKehHWXoLQ"
access_token="2942029428-YKCKJL3QFOue7z0svpTAHGJeRC4pD7LrLlPDqWM"
access_token_secret="YcHvkLJNzEfNzqDSHQE1Nt5KPFhaYo164RzwOJbo0MBzc"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def post_twitter_crsq(znlink, link, title, tags):
    for tag in tags:
        if tag.replace('-',' ') in title.lower():
	    tag = tag.replace('-',' ')
            title = title.replace(" "+tag, " #"+tag)
            title = title.replace(" "+tag.title(), " #"+tag.title())
            title = title.replace(" "+tag.capitalize(), " #"+tag.capitalize())
            title = title.replace(" "+tag.upper(), " #"+tag.upper())

    tweet = title + " " + link + " " + znlink + " #ZippedNews"
    api.update_status(status=tweet)
    return


