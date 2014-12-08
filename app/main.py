# -*- coding: utf-8 -*-	

import sys, json, security
from datetime import datetime
from functions import *

sys.path.append("../deps/")
import pylast

reload(sys)
sys.setdefaultencoding("utf-8")

#set date formatting to create datetime objects
date_format = "%d %b %Y %X"


if __name__ == '__main__':

	#refresh music list in case there are any new songs
	musiclist = refreshSongList()

	#fetch user, this would ordinarily be from a database in a web app
	user = {"userid": "8717-9975", "lastchecked": datetime.strptime("04 Dec 2014 19:38:21", date_format), "lfm_user": LFM_USER, "lfm_pwd": LFM_PWD}

	#obviously this will already be hashed in the deployed version
	password_hash = pylast.md5(user["lfm_pwd"])

	#todo: move this into user object
	lfm_object = pylast.LastFMNetwork(api_key = LFM_APIKEY, api_secret =
	LFM_SECRET, username = user["lfm_user"], password_hash = password_hash)

	#test if we hustlin'
	track = lfm_object.get_track("Rick Ross", "Hustlin'")
	track.love()

	#get user's last 25 played songs from the server
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
			songLookup(musiclist, stripSongURL(song))
			print "%s: %s" % (song["song_info/_text"], song["timestamp"])

	last_checked = datetime.now()
