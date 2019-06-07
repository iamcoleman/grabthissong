# Python
import json
import pprint
import string
import random
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
username = '**********'
scope = ''
client_id = ''**********''
client_secret = ''**********''
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
    if results['tracks']['items']:
        searchSongName = results['tracks']['items'][0]['name']
        #pprint.pprint('Name: ' + searchSongName)
        searchSongURL = results['tracks']['items'][0]['external_urls']['spotify']
        #pprint.pprint('URL: ' + searchSongURL)
    else:
        searchSongName = 'none'
        searchSongURL = 'none'
    return searchSongName, searchSongURL

def searchForAlbum(albumName):
    results = spotify.search(q=albumName, type='album')
    if results['albums']['items']:
        searchAlbumName = results['albums']['items'][0]['name']
        #pprint.pprint(results['albums']['items'][0]['name'])
        searchAlbumURL = results['albums']['items'][0]['external_urls']['spotify']
        #pprint.pprint(results['albums']['items'][0]['external_urls']['spotify'])
    else:
        searchAlbumName = 'none'
        searchAlbumURL = 'none'
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

def tweetRandomSong(status):
    numberOfLetters = random.randint(1, 2)
    numberOfSpaces = random.randint(1, 2)
    vowels = 'aeiou'
    searchString = ''
    for i in range(numberOfSpaces):
        for j in range(numberOfLetters):
            searchString += random.choice(vowels)
        searchString += ' '
    randomOffset = str(random.randint(1, 1000))
    results = spotify.search(q=searchString, offset=randomOffset, type='track')
    # if no results then re-do
    while not results['tracks']['items']:
        searchString = ''
        for i in range(numberOfSpaces):
            for j in range(numberOfLetters):
                searchString += random.choice(vowels)
            searchString += ' '
        randomOffset = str(random.randint(1, 1000))
        results = spotify.search(q=searchString, offset=randomOffset, type='track')
    # tweet back details
    randomSongName = results['tracks']['items'][0]['name']
    #pprint.pprint('Name: ' + searchSongName)
    randomSongArtist = results['tracks']['items'][0]['artists'][0]['name']
    #pprint.pprint(results['tracks']['items'][0]['artists']['name'])
    randomSongURL = results['tracks']['items'][0]['external_urls']['spotify']
    #pprint.pprint('URL: ' + searchSongURL)
    tweetBody = 'Here is a random song for you! ' + randomSongName + ' by ' + randomSongArtist + ' ' + randomSongURL
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
    elif 'random song' in tweetLower:
        print('Tweet includes "random song"')
        tweetRandomSong(status)
    else:
        print('No target words in tweet')
        tweetBody = 'For a full list of commands, please visit https://pastebin.com/SbCwp8Js'
        reply(tweetBody, status)


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
