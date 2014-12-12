# -*- coding: utf-8 -*-	
import sys, json
from datetime import datetime
from security import *
sys.path.append("../deps/")
import pylast
from filelock import FileLock

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

#checks if user already exists in the database
def checkExistingUser(user, database):
	for player in database:
		if player["userid"] == user["userid"]:
			return "true"
	return "false"

#delete user from database
def deleteUser(userid, reason):
	lock = FileLock('userlist.json')
	lock.acquire()
	#open player list and check existing players
	data_file  = open("userlist.json", 'r+')
	database = json.load(data_file)
	for user in database:
		if user['userid'] == userid:
			with open('errorlog.txt', 'a') as errorlog:
				errorlog.write("\nDeleted user %s. Reason: %s." % (userid, reason))
			database.remove(user)
	data_file.close()
	new_datafile  = open("userlist.json", 'w+')
	json.dump(database, new_datafile)
	lock.release

#adds user to json list
def createUser(userid, network, lfm_user, lfm_pwd):

	user  = {"userid": userid, "network": network, "lfm_session": sessionKeyGen(lfm_user, lfm_pwd), "lastchecked": datetime.now().strftime(date_format), "delete": "false"}

	if(user["lfm_session"]) == "INVALID":
		#lastfm credentials are invalid, alert the user
		pass
	else:
		lock = FileLock('userlist.json')
		lock.acquire()
		
		#open player list and check existing players
		data_file  = open("userlist.json", 'r+')
		database = json.load(data_file)
		if checkExistingUser(user, database) == "true":
			print "User already exists!"
		else:
			#append user and regenerate database
			database.append(user)
			data_file.close()
			new_datafile = open("userlist.json", 'w+')
			json.dump(database, new_datafile)

		lock.release()

#updates user's 'lastchecked' element, mostly copied from deleteUser
def updateLastChecked(user):
	lock = FileLock('userlist.json')
	lock.acquire()
	#open player list and check existing players
	data_file  = open("userlist.json", 'r+')
	database = json.load(data_file)
	for user in database:
		if user['userid'] == userid:
			user['lastchecked'] = datetime.now().strftime(date_format)
	data_file.close()
	new_datafile  = open("userlist.json", 'w+')
	json.dump(database, new_datafile)
	lock.release