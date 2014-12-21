# -*- coding: utf-8 -*-	

import sys, json, secrets, threading, pymongo
from datetime import datetime, timedelta
from functions import *
from usermanager import *
import pylast

reload(sys)
sys.setdefaultencoding("utf-8")

#set date formatting to create datetime objects
date_format = "%d %b %Y %X"

def iidxScrobble(user, lfm_object):
	#make this method run every n seconds
	
	#get user's last 50 played songs from the server
	playerlist = scrapeData(user["userid"], user["network"])

	if playerlist == "ERROR":
		print "Not scrobbling for player %s." % user['userid']
		markUser(user['userid'], 'NETWORK ERROR')
		return

	#iterate through songs in list
	for song in playerlist:

		#make sure the song hasn't already been checked
		
		#this time is incremented by 5 hours to compensate for being in EST
		songtime = datetime.strptime(song['timestamp'], date_format)+timedelta(hours=5)
		lastchecked = datetime.strptime(user['lastchecked'], date_format)

		#if we reach our 'lastchecked' time, then obviously there's no use checking the 
		#older songs
		if lastchecked >= songtime:
			break
		#if we see a song with misscount of -1, the user did not play it to completion and 
		#therefore it should not be scrobbled
		elif song['miss_count'] == -1:
			pass
		#if we've reached this point, this song should be scrobbled!
		else:
			songinfo = songLookup(stripSongURL(song, user["network"]))
			artist_name = songinfo["artist"]
			song_name = songinfo["title"]
			submit_time = int((songtime - datetime(1970,1,1)).total_seconds())

			print "		scrobbling %s: %s for player %s" % (song_name, submit_time, user['userid'])
			lfm_object.scrobble(artist=artist_name, title=song_name, timestamp=submit_time)

	#finally, update user's 'lastchecked' element
	updateLastChecked(user['userid'])

if __name__ == '__main__':
	#generate cookies
	generateCookies()

	for user in getDatabase().users.find({'status': 'working', 'network': 'ps'}):
		#make sure last.fm still works for this user
		try:
			lfm_object = pylast.LastFMNetwork(api_key = LFM_APIKEY, api_secret = LFM_SECRET, session_key = user['lfm_session'])
		except pylast.WSError:
			print "Error connecting to last.fm"
			markUser(user['userid'], 'LASTFM ERROR')
		#if it works, go ahead and check the tracklist
		else:
			iidxScrobble(user, lfm_object)