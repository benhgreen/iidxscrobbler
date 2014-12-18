# -*- coding: utf-8 -*-	
import sys, json, pylast, os
from datetime import datetime
from secrets import *
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding("utf-8")
date_format = "%d %b %Y %X"

#get lastfm session key for a username and password
def sessionKeyGen(lfm_user, lfm_pwd):
	global lfm_object
	try:
		lfm_object = pylast.LastFMNetwork(api_key = LFM_APIKEY, api_secret = LFM_SECRET, username = lfm_user, password_hash = pylast.md5(lfm_pwd))
	except pylast.WSError:
		print("Invalid username/password.") 
		return "INVALID"
	else:
		return getattr(lfm_object, 'session_key')

#returns true if user already exists in the database
def checkExistingUser(userid, network):
	if(getDatabase().users.find_one({"userid": userid, "network": network})) != None:
		return True
	else:
		return False
		
#mark user for later deletion if calls to their PS/PW/last.fm profile don't work
def markUser(userid, reason):
	with open('errorlog.txt', 'a') as errorlog:
		errorlog.write("\nMarked user %s for deletion. Reason: %s" % (userid, reason))
	getDatabase().users.update(
		{'userid': userid},
		{
			'$set':{
					'status': reason
			}
		})

#adds user to json list
def createUser(userid, network, lfm_user, lfm_pwd):

	#verify last.fm credentials
	lfm_session = sessionKeyGen(lfm_user, lfm_pwd)
	if(lfm_session) == "INVALID":
		#lastfm credentials are invalid, alert the user
		pass
	else:
		#create user and insert into database
		getDatabase().users.insert(
			{
				"userid": userid,
				"network": network,
				"lfm_session": lfm_session,
				"lfm_username": lfm_user,
				"lastchecked": datetime.now().strftime(date_format),
				"status": "working"
			})

#updates user's 'lastchecked' element, mostly copied from deleteUser
def updateLastChecked(userid):
	getDatabase().users.update(
		{'userid': userid},
		{
			'$set':{
					'lastchecked': datetime.now().strftime(date_format)
			}
		})

#initialize MongoClient object and return database
def getDatabase():
	client = MongoClient(os.environ('MONGODB_URL'))
	return client.userlist