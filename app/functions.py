# -*- coding: utf-8 -*-	

import sys, httplib, urllib, importio, latch
from security import *

reload(sys)
sys.setdefaultencoding("utf-8")

songdata = None
playerdata = None

#scrape data from import.io
def scrapeData(userid):
	client = clientGen()
	client.connect()
	queryLatch = latch.latch(1)

	global target_url, connector_guid

	#if the userid is 'refresh_music', this method will update the music library
	if userid == "refresh_music":
		print "REFRESHING"
		target_url = "http://webui.programmedsun.com/iidx/0/music"
		connector_guid = "e53e03d2-1468-4ebb-8fe9-2ef64de33db2"
	else:
		target_url = "http://webui.programmedsun.com/iidx/0/players/%s/scores" % userid
		connector_guid = "9247219f-a36f-4e6b-85b0-1956eff5836d"
	
	#callback to export the returned data
	def callback(query, message):
		global data
		
		if message["type"] == "DISCONNECT":
			print "Query in progress when library disconnected"
		if message["type"] == "MESSAGE":
			if "errorType" in message["data"]:
				print "Got an error!" 
			else:
				print "Got data!"
				data = (message["data"]["results"])
		
		if query.finished(): 
			queryLatch.countdown()

	client.query({
		"connectorGuids":[
			connector_guid
		],
		"input": {
			"webpage/url": target_url
		},
		"additionalInput": {
			connector_guid: {
				"domainCredentials": {
					"webui.programmedsun.com": {
						"username": getPSuser(),
						"password": getPSpwd(),
					}
				}
			}
		}
	}, callback)

	queryLatch.await()
	client.disconnect()
	
	return data

# refreshes song list and converts to dictionary where key is songid
# and value is tuple (title, artist)
def refreshSongList():

	songlist = {'songid' : 'songinfo'}
	raw_data = scrapeData('refresh_music')

	for song in raw_data:

		songid = stripSongURL(song)
		songinfo = (song["song_info/_text"], song["artist"])

		songlist[songid] = songinfo


	return songlist


#strip song url to its id
def stripSongURL(song):
	songurl = song["song_info/_source"][14:]
	return songurl[:songurl.index('/')]


#return song info from main data bank
def songLookup(songdb, songid):
	return songdb[songid]