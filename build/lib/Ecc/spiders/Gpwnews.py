import scrapy


class GpwnewsSpider(scrapy.Spider):
    name = "Gpwnews"
    allowed_domains = ["www.gpw.pl"]
    start_urls = ["https://www.gpw.pl/all-news"]

    def parse(self, response):
        pass
