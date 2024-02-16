import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo

class GPWMongoDBPipeline:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://mongo:PNJg1god7O4VAMMr@cluster0.p6vsysp.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
        self.db = self.client["Gpwnewsscrapper"]
        self.collection = self.db["gpw news testing"]
        
        # Create a unique index on the "title" field
        self.collection.create_index("title", unique=True)
        
    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item

class GPWSpider(scrapy.Spider):
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
        "ROBOTSTXT_OBEY": False,
        "CONCURRENT_REQUESTS": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 16,
        "CONCURRENT_REQUESTS_PER_IP": 16,
        "DOWNLOAD_DELAY": 3,
    }

    name = "gpw_spider"
    start_urls = [
        "https://www.gpw.pl/all-news/",
    ]

    def start_requests(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=chrome_options)

        for url in self.start_urls:
            driver.get(url)
            yield scrapy.Request(url, self.parse, meta={"driver": driver})

    def parse(self, response):
        driver = response.meta["driver"]
        print(response.body)

        while True:
            # Extracting and printing the data from the current page
            elements = driver.find_elements(By.CSS_SELECTOR, '.shortNews ul.list li')
            for element in elements:
                yield {
                    'header': element.find_element(By.CSS_SELECTOR, 'span').text,
                    'title': element.find_element(By.CSS_SELECTOR, 'h4').text,
                    'body': element.find_element(By.CSS_SELECTOR, 'p').text
                }

            # Extracting the "Show previous" link
            show_previous_link = driver.find_element(By.CSS_SELECTOR, '.text-center a.more')

            # Click the "Show previous" link
            show_previous_link.click()

            try:
                # Wait for the new page to load (adjust the timeout and condition as needed)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.shortNews ul.list li'))
                )
            except Exception:
                # Break the loop if the "Show previous" link is not available
                break
