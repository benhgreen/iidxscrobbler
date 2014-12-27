# -*- coding: utf-8 -*-	

import sys, json, secrets, threading, pymongo, os
from datetime import datetime, timedelta
from functions import *
from usermanager import *
import pylast

reload(sys)
sys.setdefaultencoding("utf-8")

#set date formatting to create datetime objects
date_format = "%d %b %Y %X"

def iidxScrobble(user, lfm_object):
	#get user's last 50 played songs from the server
	playerlist = scrapeData(user["userid"], int(user["version"]))

	if playerlist == "ERROR":
		print "Not scrobbling for player %s." % user['userid']
		markUser(user, 'NETWORK ERROR')
		return

	#iterate through songs in list
	for song in reversed(playerlist):
		
		#this time is incremented by 5 hours to compensate for being in EST
		songtime = datetime.strptime(song['timestamp'], date_format)+timedelta(hours=5)
		lastchecked = datetime.strptime(user['lastchecked'], date_format)

		#ignore songs that we already have scrobbled
		if lastchecked >= songtime:
			pass
		#if we see a song with misscount of -1, the user did not play it to completion and 
		#therefore it should not be scrobbled
		elif song['miss_count'] == -1:
			pass
		#if we've reached this point, this song should be scrobbled!
		else:
			songinfo = songLookup(stripSongURL(song))
			artist_name = songinfo["artist"]
			song_name = songinfo["title"]
			submit_time = int((songtime - datetime(1970,1,1)).total_seconds())

			print "		scrobbling %s: %s for player %s" % (song_name, submit_time, user['userid'])
			try:
				lfm_object.scrobble(artist=artist_name, title=song_name, timestamp=submit_time)
			except pylast.WSError:
				markUser(user, 'LASTFM SCROBBLE ERROR')
				return


	#finally, update user's 'lastchecked' element
	updateLastChecked(user['userid'], user['version'])

if __name__ == '__main__':
	#test cookies
	testCookies(['ps', 'pw'])

	for user in getDatabase().users.find({'status': 'initializeme'}):

		#if we already have an instance of this lfm user working, just copy that session key
		usercheck = getDatabase().users.find_one({'lfm_username': user['lfm_username'], 'status': 'working'})
		if (usercheck != None):
			getDatabase().users.update(
			{'userid': user['userid'], 'version': user['version']},
			{
				'$set':{
					'lfm_session': usercheck['lfm_session'],
					'status': 'working'
				},
				'$unset':{
					'lfm_url': True
				}
			})		
		else:
			#give the user 15 minutes to authenticate our app
			if (datetime.strptime(user['lastchecked'], date_format)+timedelta(minutes=10)) <= datetime.now():
				lfmInit(user)

	for user in getDatabase().users.find({'status': 'working'}):

		#make sure last.fm still works for this user
		try:
			lfm_object = pylast.LastFMNetwork(api_key = os.environ.get('LFM_APIKEY'), api_secret = os.environ.get('LFM_SECRET'), session_key = user['lfm_session'])
		except pylast.WSError:
			print "Error connecting to last.fm"
			markUser(user, 'LASTFM ERROR')
		#if it works, go ahead and check the tracklist
		else:
			iidxScrobble(user, lfm_object)