# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class PhimPipeline(object):
    collection_name = 'movie_detail'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'event_data')
        )

    def open_spider(self, spider):
        # self.collection_name = spider.name
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        # disable drop by default
        # self.db.drop_collection(self.collection_name)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        #  filter duplicate event by url
        self.db[self.collection_name].update({'url': item['url']}, item, upsert=True)
        return item
