# Libraries
import tweepy
# Files
from API.twitter_keys import getKeys

#######################################
# Get Twitter API keys
access_token, access_secret, consumer_key, consumer_secret = getKeys()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
tiger = tweepy.API(auth)
#######################################


def reply(body, status):
	user = status.author.screen_name
	reply_id = status.id
	juice = body
	reply = "@"+user+" "+juice
	tiger.update_status(reply, in_reply_to_status_id=reply_id)
	print("Reply:")
	print(reply)


#######################################
def replyTigerBack(status):
	lower = status.text.lower()
	if "tiger back" in lower:
		print("Tweet includes tiger back...")
		reply("He's back", status)

#######################################


#######################################
class StreamListener(tweepy.StreamListener):

	def on_status(self, status):
		print("\nIncoming tweet by "+status.author.screen_name+":")
		print(status.text)
		replyTigerBack(status)


	def on_error(self, status_code):
		if status_code == 420:
			return False
#######################################


#######################################
stream_listener = StreamListener()
print("Stream Starting...\n")
stream = tweepy.Stream(auth=tiger.auth, listener=stream_listener)
stream.filter(track=["@is_tiger_back"])
#######################################
