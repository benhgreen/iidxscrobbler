# -*- coding: utf-8 -*-	
import sys, json
from datetime import datetime
from security import *
from pymongo import MongoClient
sys.path.append("../deps/")
import pylast

reload(sys)
sys.setdefaultencoding("utf-8")
date_format = "%d %b %Y %X"

#get lastfm session key for a username and password
def sessionKeyGen(lfm_user, lfm_pwd):
	global lfm_object
	try:
		lfm_object = pylast.LastFMNetwork(api_key = LFM_APIKEY, api_secret = LFM_SECRET, username = LFM_USER, password_hash = pylast.md5(lfm_pwd))
	except pylast.WSError:
		print("Invalid username/password.") 
		return "INVALID"
	else:
		return getattr(lfm_object, 'session_key')

#returns true if user already exists in the database
def checkExistingUser(userid, db):
	if(db.users.find_one({"userid": userid})) != None:
		return True

#mark user which can't be accessed, either via last.fm or scraping
def markUser(userid, reason):
	with open('errorlog.txt', 'a') as errorlog:
		errorlog.write("\nMarked user %s. Reason: %s" % (userid, reason))
	getDatabase().users.update(
		{'userid': userid},
		{
			'$set':{
					'status': reason
			}
		})


#adds user to json list
def createUser(userid, network, lfm_user, lfm_pwd):

	if checkExistingUser(userid, getDatabase()):
		print "User already exists!"
		return "EXISTS"

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
	client = MongoClient()
	return client.db