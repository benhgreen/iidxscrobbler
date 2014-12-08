# -*- coding: utf-8 -*-	

import sys, json
from datetime import datetime
from functions import *

reload(sys)
sys.setdefaultencoding("utf-8")

#set date formatting to create datetime objects
date_format = "%d %b %Y %X"


#refresh music list in case there are any new songs
musiclist = refreshSongList()

#fetch user, this would ordinarily be from a database in a web app
user = {"userid": "8717-9975", "lastchecked": datetime.strptime("04 Dec 2014 19:38:21")}

#get user's last 25 played songs from the server
playerlist = scrapeData(user["userid"])

#iterate through songs in list
for song in playerlist:
	
	#make sure the song hasn't already been checked
	songtime = datetime.strptime(song["timestamp"], date_format)
	if(user["lastchecked"] >= songtime || song["clear_status"]):
		pass
	else:
		#these songs should be scrobbled!
		songLookup(musiclist, stripSongURL(song))
		print "%s: %s" % (song["song_info/_text"], song["timestamp"])

last_checked = datetime.now()
