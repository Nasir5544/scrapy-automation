# ecc_project/spiders/ecc_spider.py
import scrapy
from Ecc.items import EccItem
from Ecc.itemloaders import EccItemLoader
import pymongo

class EccSpider(scrapy.Spider):
    custom_settings = {
       'ITEM_PIPELINES': {
            'Ecc.pipelines.EccPipeline': 100,
           # 'Ecc.pipelines.GPWMongoDBPipeline': 200,
            'Ecc.pipelines.MongoDBPipeline': 300,
           # 'Ecc.pipelines.AthexnewsDBPipeline': 400,
        }
         
    }
  
    name = "ecc"
    allowed_domains = ["www.ecc.de"]
    start_urls = ["https://www.ecc.de/en/newsroom/circulars"]
   

    def parse(self, response):
        for row in response.css('table tr'):
            h3 = row.css('h3::text').get()
            if h3:
                item_loader = EccItemLoader(item=EccItem(), selector=row)
                item_loader.add_value('title', h3)
                date = row.css('time::text').get().strip()
                if date:
                    item_loader.add_value('date', date)
                link = row.css('a::attr(href)').get()
                if link:
                    item_loader.add_value('link', response.urljoin(link))

               # yield item_loader.load_item()
                #yield response.follow(link, callback=self.parse_detail, meta={'item_loader': item_loader})
               
                
                item = item_loader.load_item()
                yield item

                # Follow the link to the detail page and pass the item to the parse_detail method
                yield response.follow(link, callback=self.parse_detail, meta={'item': item})
               # yield response.follow(item['url'], callback=self.parse_detail, meta={'item': item})

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
    
    def parse_detail(self, response):
        item = response.meta['item']
        
        # Extract the description from the detail page using ItemLoader
        item_loader = EccItemLoader(item=item, selector=response)
        # Use getall() to get all the text within <p> tags
        summary = response.css('p::text').getall()
        # Join the list of description text with line breaks to form a single string
        summary_text = ''.join(summary)
        #
        # Add the combined description text to the 'description' field
        item_loader.add_value('summary',  summary_text)

        yield item_loader.load_item()