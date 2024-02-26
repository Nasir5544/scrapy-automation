# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# ecc_project/items.py
import scrapy


class EcccircularsdataItem(scrapy.Item):
    # define the fields for your item here like:
     date = scrapy.Field()
     title = scrapy.Field()
     titlelink = scrapy.Field()
     pdflink = scrapy.Field()  
     description = scrapy.Field()
     circularwithdate = scrapy.Field()

    