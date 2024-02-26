# ecc_project/item_loaders.py
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

class ECCProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    circularwithdate_in = MapCompose(lambda x: x.strip().split(" | ")[0])
    title_in = MapCompose(lambda x: x.strip().split(" | ")[1] if len(x.strip().split(" | ")) > 1 else x.strip())
    date_in = MapCompose(lambda x: x.strip().split("\n")[0])
    description_in = MapCompose(lambda x: x.replace("\n", "").replace("\xa0", "").strip())
    titlelink_in = MapCompose(lambda x: 'https://www.ecc.de' + x)

    
    
    
