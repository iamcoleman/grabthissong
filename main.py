# Python
import json
import pprint
# Libraries
import tweepy
import spotipy
import spotipy.oauth2 as oauth2
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
username = '12156140455'
scope = ''
client_id = '49ff0f2a990a4af2886eda66daeca7cf'
client_secret = 'afc1335ebccc432381bd68acad5a7994'
redirect_uri = 'http://localhost/'

"""
## UTIL METHOD ##
# used for getting personal info
token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)
spotify = spotipy.Spotify(auth=token)
result = spotify.search('eminem')
pprint.pprint(result)
"""

## OAUTH 2 ##
token = util.oauth2.SpotifyClientCredentials(client_id, client_secret)
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)


#######################
## SPOTIPY FUNCTIONS ##
#######################

def searchForTrack(songName):
    results = spotify.search(q=songName, type='track')
    searchSongName = results['tracks']['items'][0]['name']
    #pprint.pprint('Name: ' + searchSongName)
    searchSongURL = results['tracks']['items'][0]['external_urls']['spotify']
    #pprint.pprint('URL: ' + searchSongURL)
    return searchSongName, searchSongURL

def searchForAlbum(albumName='Marshall Mathers'):
    results = spotify.search(q=albumName, type='album')
    searchAlbumName = results['albums']['items'][0]['name']
    #pprint.pprint(results['albums']['items'][0]['name'])
    searchAlbumURL = results['albums']['items'][0]['external_urls']['spotify']
    #pprint.pprint(results['albums']['items'][0]['external_urls']['spotify'])
    return searchAlbumName, searchAlbumURL

def tweetSearchForSong(status):
    tweetLower = status.text.lower()
    splitTweet = tweetLower.split()
    target = 'song'
    for i, word in enumerate(splitTweet):
        if word == target:
            if splitTweet[i+1]:
                songName = splitTweet[i+1:]
    songName = ' '.join(songName)
    searchSongName, searchSongURL = searchForTrack(songName)
    tweetBody = 'Here is ' + searchSongName + ' for you! ' + searchSongURL
    reply(tweetBody, status)

def tweetSearchForAlbum(status):
    tweetLower = status.text.lower()
    splitTweet = tweetLower.split()
    target = 'album'
    for i, word in enumerate(splitTweet):
        if word == target:
            if splitTweet[i+1]:
                albumName = splitTweet[i+1:]
    albumName = ' '.join(albumName)
    searchAlbumName, searchAlbumURL = searchForAlbum(albumName)
    tweetBody = 'Here is ' + searchAlbumName + ' for you! ' + searchAlbumURL
    reply(tweetBody, status)



#######################
## Twitter Functions ##
#######################

def reply(body, status):
	user = status.author.screen_name
	reply_id = status.id
	juice = body
	reply = "@"+user+" "+juice
	GTS.update_status(reply, in_reply_to_status_id=reply_id)
	print("Reply:")
	print(reply)



####################
## GRAB THIS SONG ##
####################

def GrabThisSong(status):
    # Turn the tweet text to lower case
    # and remove @grabthissong
    fullTweetLower = status.text.lower()
    fullTweetLower = fullTweetLower.split()
    tweetLower = []
    for word in fullTweetLower:
        if word != '@grabthissong':
            tweetLower.append(word)
    tweetLower = ' '.join(tweetLower)
    # decision tree
    if 'search for song' in tweetLower:
        print('Tweet includes "search for song"')
        tweetSearchForSong(status)
    elif 'search for album' in tweetLower:
        print('Tweet includes "search for album"')
        tweetSearchForAlbum(status)


###########################
## STEAMING THE TIMELINE ##
###########################

class StreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print("\nIncoming tweet by "+status.author.screen_name+":")
		print(status.text)
		GrabThisSong(status)
	def on_error(self, status_code):
		if status_code == 420:
			return False

stream_listener = StreamListener()
print("Stream Starting...\n")
stream = tweepy.Stream(auth=GTS.auth, listener=stream_listener)
stream.filter(track=["@GrabThisSong"])
