# -*- coding: utf-8 -*-	

import sys, json, security, threading
from threading import Timer
from datetime import datetime
from functions import *

sys.path.append("../deps/")
import pylast

reload(sys)
sys.setdefaultencoding("utf-8")

#set date formatting to create datetime objects
date_format = "%d %b %Y %X"

def iidxScrobble(user, lfm_object):
	#make this method run every n seconds
	threading.Timer(150.0, iidxScrobble, [user, lfm_object]).start()
	
	#get user's last 50 played songs from the server
	playerlist = scrapeData(user["userid"])

	#iterate through songs in list
	for song in playerlist:

		#make sure the song hasn't already been checked
		songtime = datetime.strptime(song["timestamp"], date_format)

		#only scrobble songs played since we last checked
		#also only play songs which were played to completion
		if(user["lastchecked"] >= songtime or song["miss_count"] == -1):
			pass
		else:
			#these songs should be scrobbled!
			(song_name, artist_name) = songLookup(musiclist, stripSongURL(song))
			submit_time = int((songtime - datetime(1970,1,1)).total_seconds())

			print "scrobbling %s: %s" % (song["song_info/_text"], song["timestamp"])
			lfm_object.scrobble(artist=artist_name, title=song_name, timestamp=submit_time)

	
	user["lastchecked"] = datetime.now()

if __name__ == '__main__':

	#refresh music list in case there are any new songs
	musiclist = refreshSongList()

	#fetch user, this would ordinarily be from a database in a web app
	user = {"userid": "8717-9975", "lastchecked": datetime.strptime("08 Dec 2014 22:42:00", date_format), "lfm_user": LFM_USER, "lfm_pwd": LFM_PWD}

	#obviously this will already be hashed in the deployed version
	password_hash = pylast.md5(user["lfm_pwd"])

	#todo: move this into user object
	lfm_object = pylast.LastFMNetwork(api_key = LFM_APIKEY, api_secret =
	LFM_SECRET, username = user["lfm_user"], password_hash = password_hash)

	iidxScrobble(user, lfm_object)