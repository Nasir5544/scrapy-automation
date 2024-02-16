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
    def __init__(self):
        self.client = MongoClient("mongodb+srv://mongo:PNJg1god7O4VAMMr@cluster0.p6vsysp.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
        self.db = self.client["scrapper"]
        self.collection = self.db["Ecc news testing"]
        
        # Create a unique index on the "title" field
        self.collection.create_index("title", unique=True)
        
    def process_item(self, item, spider):
        try:
            # Attempt to insert the item into MongoDB
            self.collection.insert_one(dict(item))
        except pymongo.errors.DuplicateKeyError as e:
            # Handle duplicate key error (e.g., log the error and skip insertion)
            print(f"Duplicate key error: {e}")
            pass
        
        return item




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



class AthexnewsDBPipeline:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://mongo:PNJg1god7O4VAMMr@cluster0.p6vsysp.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
        self.db = self.client["Athexnewsscrapper"]
        self.collection = self.db["gpw news testing"]
        
        # Create a unique index on the "title" field
        self.collection.create_index("title", unique=True)
        
    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item             


