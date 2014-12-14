import logging, json, importio, latch, os

def clientGen():
	return importio.importio(user_id=os.environ['IIO_USER'], api_key=os.environ['IIO_API'], host="https://query.import.io")

LFM_APIKEY = os.environ['LFM_APIKEY']
LFM_SECRET = os.environ['LFM_SECRET']

PW_USER = os.environ['PW_USER']
PW_PWD = os.environ['PW_PWD']

PS_USER = os.environ['PS_USER']
PS_PWD = os.environ['PS_PWD']