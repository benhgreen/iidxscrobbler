from scrapy.spider import Spider

#ask which version of iidx playing (0 = omnimix / 20 tricoro)
#currently hard coded for one user and one song
#need to create a dummy account to login to programmedsun before running scrapy
class iidxSpider(Spider):
    name = "iidx"
    allowed_domains = ["webui.programmedsun.com/"]
    start_urls = [
        "http://webui.programmedsun.com/iidx/0/players/8717-9975/scores",
        "http://webui.programmedsun.com/iidx/0/music/17022/h7"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)