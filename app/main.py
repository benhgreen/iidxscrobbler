# -*- coding: utf-8 -*-	

import sys, json, security, threading
from threading import Timer
from datetime import datetime
from functions import *

from random import shuffle

sys.path.append("../deps/")
import pylast

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

if __name__ == '__main__':
	global user
	generateCookies()
	
	musiclist = {'pw': None, 'ps': None}

	#refresh music list in case there are any new songs
	musiclist['pw'] = refreshSongList('pw')
	musiclist['ps'] = refreshSongList('ps')

	userarray = []

	#load userlist
	pw_list = json.load(open('pwlist.json'))
	ps_list = json.load(open('pslist.json'))
	
	for player in pw_list["data"]:
		userid = player["userid"][0]
		username = player["djname"][0]


		userarray.append({"userid": userid, "lastchecked": datetime.strptime("08 Dec 2014 22:42:00", date_format), "lfm_user": LFM_USER, "lfm_pwd": LFM_PWD, "network": 'pw', "djname": username})

	for player in ps_list["data"]:
		userid = player["userid"][0]
		username = player["djname"][0]

		userarray.append({"userid": userid, "lastchecked": datetime.strptime("08 Dec 2014 22:42:00", date_format), "lfm_user": LFM_USER, "lfm_pwd": LFM_PWD, "network": 'ps', "djname": username})


	shuffle(userarray)

	for user in userarray:
		#todo: move this into user object
		lfm_object = pylast.LastFMNetwork(api_key = LFM_APIKEY, api_secret =
		LFM_SECRET, username = user["lfm_user"], password_hash = user["lfm_pwd"])
		
		
		iidxScrobble(user, lfm_object, musiclist[user["network"]])