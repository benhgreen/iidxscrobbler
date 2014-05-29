# Scraping Song ID and Song Title to be scrobbled on last.fm
# Song ID can access Artist and Genre

from scrapy.item import Item, Field

class IidxscrobblerItem(Item):
    songtitle = Field()
    songid = Field()
    pass
