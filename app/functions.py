# -*- coding: utf-8 -*-	

import sys, httplib, urllib, importio, latch, string
from security import *

reload(sys)
sys.setdefaultencoding("utf-8")

songdata = None
playerdata = None

#scrape data from import.io
def scrapeData(userid, network):
	client = clientGen()
	client.connect()
	queryLatch = latch.latch(1)

	global target_url, connector_guid, short_url

	#if the userid is 'refresh_music', this method will update the music library, otherwise it will check the user's recently played
	#stuff for scraping programmed sun
	if(network == 'ps'):
		short_url = "webui.programmedsun.com"
		if userid == "refresh_music":
			print "refreshing PS song list..."
			target_url = "http://webui.programmedsun.com/iidx/0/music"
			connector_guid = "e53e03d2-1468-4ebb-8fe9-2ef64de33db2"
		else:
			print "refreshing PS player %s tracklist..." % userid
			target_url = "http://webui.programmedsun.com/iidx/0/players/%s/scores" % userid
			connector_guid = "9247219f-a36f-4e6b-85b0-1956eff5836d"
	#stuff for scraping programmed world
	elif(network == 'pw'):
		short_url = "programmedworld.net"
		if(userid == "refresh_music"):
			print "refreshing PW song list..."
			target_url = "https://programmedworld.net/iidx/22/music"
			connector_guid = "7d120ee9-000f-43f1-961a-17e4ff45771e"
		else:
			print "refreshing PW player %s tracklist..." % userid
			target_url = "https://programmedworld.net/iidx/22/players/%s/scores" % userid
			connector_guid = "329e12e0-85ea-4961-83b6-a1156e25d46a"
	#callback to export the returned data
	def callback(query, message):
		global data
		
		if message["type"] == "DISCONNECT":
			print "Query in progress when library disconnected"
		if message["type"] == "MESSAGE":
			if "errorType" in message["data"]:
				print "Got an error!" 
				print json.dumps(message["data"], indent = 4)
			else:
				print "Got data!"
				data = (message["data"]["results"])
		
		if query.finished(): 
			queryLatch.countdown()

	#import.io's template queries sure are awesome
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
					short_url: {
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
def refreshSongList(network):

	songlist = {'songid' : 'songinfo'}
	raw_data = scrapeData('refresh_music', network)

	for song in raw_data:

		songid = stripSongURL(song)
		#strip out stupid leggendaria suffix
		if "†LEGGENDARIA" in song["song_info/_text"]:
			songinfo = (string.replace(song["song_info/_text"], "†LEGGENDARIA", ""), song["artist"])
		else:
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