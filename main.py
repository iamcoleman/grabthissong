# Python
import pprint
import sys
# Libraries
import tweepy
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
# Files
from API.twitter_keys import getKeys

##########################
## Get Twitter API keys ##
##########################
access_token, access_secret, consumer_key, consumer_secret = getKeys()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
GTS = tweepy.API(auth)

#############
## Spotipy ##
#############
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

search_str = 'Muse'
result = sp.search(search_str)
pprint.pprint(result)


"""
def reply(body, status):
	user = status.author.screen_name
	reply_id = status.id
	juice = body
	reply = "@"+user+" "+juice
	GTS.update_status(reply, in_reply_to_status_id=reply_id)
	print("Reply:")
	print(reply)



###########################
## STEAMING THE TIMELINE ##
###########################

class StreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print("\nIncoming tweet by "+status.author.screen_name+":")
		print(status.text)
		replyGTSBack(status)
	def on_error(self, status_code):
		if status_code == 420:
			return False

stream_listener = StreamListener()
print("Stream Starting...\n")
stream = tweepy.Stream(auth=GTS.auth, listener=stream_listener)
stream.filter(track=["@GrabThisSong"])
"""