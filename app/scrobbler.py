# -*- coding: utf-8 -*-	

import sys, json, security, threading
from functions import *
from threading import Timer
from datetime import datetime
from random import shuffle
from usergen import *

sys.path.append("../deps/")
import pylast
from filelock import FileLock

reload(sys)
sys.setdefaultencoding("utf-8")

#set date formatting to create datetime objects
date_format = "%d %b %Y %X"

def iidxScrobble(user, lfm_object, musiclist):
	#make this method run every n seconds
	
	#get user's last 50 played songs from the server
	playerlist = scrapeData(user["userid"], user["network"])

	if playerlist == "ERROR":
		print "Not scrobbling for player %s." % user["userid"]
		markUser(user)
		return

	#iterate through songs in list
	for song in playerlist:

		#make sure the song hasn't already been checked
		songtime = datetime.strptime(song["timestamp"], date_format)

		#if we reach our 'lastchecked' time, then obviously there's no use checking the 
		#older songs
		if user["lastchecked"] >= songtime:
			break
		#if we see a song with misscount of -1, the user did not play it to completion and 
		#therefore it should not be scrobbled
		elif song["miss_count"] == -1:
			pass
		#if we've reached this point, this song should be scrobbled!
		else:
			(song_name, artist_name) = songLookup(musiclist, stripSongURL(song, user["network"]))
			submit_time = int((songtime - datetime(1970,1,1)).total_seconds())

			print "		scrobbling %s: %s" % (song_name, song["timestamp"])
			#lfm_object.scrobble(artist=artist_name, title=song_name, timestamp=submit_time)

	user["lastchecked"] = datetime.now()

def function():
	pass


if __name__ == '__main__':
	global user
	generateCookies()

	#generate master song lists
	musiclist['pw'] = refreshSongList('pw')
	musiclist['ps'] = refreshSongList('ps')

	#load userlist
	userlist = json.load(open('userlist.json'))

	for user in userlist:
		if user["name"] != "delete":
			try:
				lfm_object = pylast.LastFMNetwork(api_key = LFM_APIKEY, api_secret = LFM_SECRET, session_key = "976d989cbae4b163af487b36e05835a0")
			except pylast.WSError:
				print "Error connecting to last.fm"
				markUser(user)
			else:
				iidxScrobble(user, lfm_object, musiclist[user["network"]])