import logging, json, importio, latch, os

def clientGen():
	return importio.importio(user_id=os.environ.get('IIO_USER'), api_key=os.environ.get('IIO_API'), host="https://query.import.io")

LFM_APIKEY = os.environ.get('LFM_APIKEY')
LFM_SECRET = os.environ.get('LFM_SECRET')

PW_USER = os.environ.get('PW_USER')
PW_PWD = os.environ.get('PW_PWD')

PS_USER = os.environ.get('PS_USER')
PS_PWD = os.environ.get('PS_PWD')