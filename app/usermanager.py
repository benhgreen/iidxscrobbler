# -*- coding: utf-8 -*-	
import sys, json, pylast, os
from datetime import datetime
from secrets import *
from functions import *
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding("utf-8")
date_format = "%d %b %Y %X"

#returns true if user already exists in the database
def checkExistingUser(userid, version):
	if(getDatabase().users.find_one({"userid": userid, "version": version})) != None:
		return True
	else:
		return False
		
#checks to see if the user exists on the server
def checkUserValidity(userid, version):
	if version < 22:
		generateCookies(['ps'])
	else:
		generateCookies(['pw'])
	if(scrapeData(userid, version) == 'ERROR'):
		return False
	return True

#mark user for later deletion if calls to their PS/PW/last.fm profile don't work
def markUser(user, reason):
	with open('errorlog.txt', 'a') as errorlog:
		errorlog.write("\nMarked user %s for deletion. Reason: %s" % (user['userid'], reason))
	getDatabase().users.update(
		{'userid': user['userid'], 'version': user['version']},
		{
			'$set':{
					'status': reason
			}
		})

#adds user to database
def createUser(userid, version, lfm_user):
	getDatabase().users.insert(
		{
			"userid": userid,
			"version": version,
			"lfm_username": lfm_user,
			"lastchecked": datetime.now().strftime(date_format),
			"status": "initializeme"
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
	client = MongoClient(os.environ.get('MONGODB_URL'))
	return client.userlist

#initialize last.fm session key for user
def lfmInit(user):
	#initialize lfm objects
	url = user['lfm_url']
	network = pylast.get_lastfm_network(os.environ.get('LFM_APIKEY'), os.environ.get('LFM_SECRET'))
	sg = pylast.SessionKeyGenerator(network)
	sg.web_auth_tokens[url] = url[(url.index('token')+6):]
	sg.api_key = os.environ.get('LFM_APIKEY')
	sg.api_secret = os.environ.get('LFM_SECRET')
	#try to authorize token
	try:
		session_key = sg.get_web_auth_session_key(user['lfm_url'])
		print session_key
	except pylast.WSError:
		print "Error authorizing user for last.fm"
		markUser(user, 'LASTFM INIT ERROR')
	else:
		getDatabase().users.update(
		{'userid': user['userid']},
		{
			'$set':{
				'lfm_session': session_key,
				'status': 'working'
			},
			'$unset':{
				'lfm_url': True
			}
		})