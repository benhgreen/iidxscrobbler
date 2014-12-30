iidxscrobbler
================

Scrobbler for various IIDX versions.

* Uses import.io to scrape user's list of played songs
* Identifies songs played to completion by checking clear status and miss count
* Scrobbles said songs via pylast (handy Python library using the last.fm API)
* User info stored with MongoDB: player ID, last.fm session key, game version
* Frontend made with Bootstrap, Tornado, Flask, and WTForms


To setup - set proper environment variables in secrets.py, use appropriate import.io scrapers(or scrapy if you so wish, but you'll likely need to tweak the structures used a bit), and run webinterface.py. Run scrobbler.py periodically for whichever network you would like to use - I have both on separate cron jobs running every 15 minutes, about 5 minutes apart from each other.