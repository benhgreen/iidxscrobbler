# -*- coding: utf-8 -*-	

import sys, json
from functions import *

reload(sys)
sys.setdefaultencoding("utf-8")

musiclist = refreshSongList()

while true:
	playerlist = scrapeData("8717-9975")

	for song in playerlist:
		songLookup(musiclist, stripSongURL(song))
		print song["timestamp"]
