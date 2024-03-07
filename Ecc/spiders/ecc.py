# ecc_project/spiders/ecc_spider.py
import scrapy
from Ecc.itemloaders import ECCProductLoader
from Ecc.items import EcccircularsdataItem



class EccSpiderSpider(scrapy.Spider):
    custom_settings = {
       'ITEM_PIPELINES': {
            'Ecc.pipelines.EccPipeline': 100,
           # 'Ecc.pipelines.GPWMongoDBPipeline': 200,
            'Ecc.pipelines.MongoDBPipeline': 300,
           # 'Ecc.pipelines.AthexnewsDBPipeline': 400,
        }
         
    }
    
    name = "Ecc_spider"
    allowed_domains = ["ecc.de"]
    start_urls = ["https://www.ecc.de/en/newsroom/circulars"]


    def parse(self, response):
       
        table_rows = response.css("table tr")
        for row in table_rows[1:11]:
            loader = ECCProductLoader(item=EcccircularsdataItem(), selector=row)

            # Use the loaders to load the item fields
            loader.add_css('date', 'time::text')
            loader.add_css('circularwithdate', 'h3::text')
            loader.add_css('title', 'h3::text')
            loader.add_css('titlelink', 'td a::attr(href)')  
            loader.add_css('pdflink', 'td.download a::attr(href)')

            #Follow the link to the detail page
            item = loader.load_item()
            
            #Print the 'title' and 'additional_title' parts
            print(item['title'])
            print(item['circularwithdate'])

            yield response.follow(item['titlelink'], self.parse_detail, meta={'item': item})

        next_page = response.css(".next a::attr(href)").get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
    
        
        # Extract the description from the detail page using ItemLoader
        item_loader = ECCProductLoader(item=item, selector=response)
        # Use getall() to get all the text within <p> tags
        descriptions = response.css('p::text').getall()
        # Join the list of description text with line breaks to form a single string
        description_text = '\n'.join(descriptions)
        # Add the combined description text to the 'description' field
        item_loader.add_value('description', description_text)

        yield item_loader.load_item()