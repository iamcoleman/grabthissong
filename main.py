# Python
import json
# Libraries
import tweepy
import spotipy
import spotipy.util as util
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
client_id = '49ff0f2a990a4af2886eda66daeca7cf'
client_secret = 'afc1335ebccc432381bd68acad5a7994'

token = util.oauth2.SpotifyClientCredentials(client_id, client_secret)
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

tids = []
track_list = []
artist_list = ['Taylor Swift','Linkin Park','Charlie Puth']
for artist in artist_list:
   print(artist)
   results = spotify.search(q=artist,limit = 50)
   for i, t in enumerate(results['tracks']['items']):
      tids.append(t['uri'])


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