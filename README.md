iidxscrobbler
================

Scrobbler for various IIDX versions.

* Uses import.io to scrape user's list of played songs
* Identifies songs played to completion by checking clear status and miss count
* Scrobbles said songs via pylast (handy Python library using the last.fm API)
* User info stored with MongoDB: player ID, last.fm session key, game version
* Frontend made with Bootstrap, Tornado, Flask, and WTForms