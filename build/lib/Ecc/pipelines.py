# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import json
from pymongo import MongoClient, InsertOne
import sys
from pymongo.server_api import ServerApi
import certifi



class EccPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    ca = certifi.where()

    # client = pymongo.MongoClient("mongodb+srv://nasir1991:YOTXkeCxNTlOBCkA@cluster0.p6vsysp.mongodb.net/")
    client = MongoClient("mongodb+srv://mongo:PNJg1god7O4VAMMr@cluster0.p6vsysp.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
    db = client["scrapper"]
    collection = db["Ecc news"]

    
    
    with open('finalone.json',  encoding='utf-8') as file:
       data = json.load(file)
       
    if isinstance(data, list):
       collection.insert_many(data)
    else:
       collection.insert_one(data)