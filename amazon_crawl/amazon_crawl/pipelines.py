# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class AmazonCrawlPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['amazon_key_list'].update({'position_num':item['position_num']},{'$set':item},True)
        # self.db[self.collection_name].insert_one(dict(item))
        return item




class MySQLPipeline(object):

    def from_crawler(cls,crawler):
        cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DB_NAME", 'scrapy_default')
        cls.HOST = crawler.settings.get("MYSQL_HOST", 'localhost')
        cls.PORT = crawler.settings.get("MYSQL_PORT", 3306)
        cls.USER = crawler.settings.get("MYSQL_USER", 'root')
        cls.PASSWD = crawler.settings.get("MYSQL_PASSWORD", 'new.1234')
        return cls()
    def open_spider(self,spider):
        self.dbpool= adbapi.ConnectionPool('pymysql', host=self.HOST, port=self.PORT, user=self.USER, passwd=self.PASSWD, db=self.MYSQL_DB_NAME, charset='utf8')
    def close_spider(self,spider):
        self.dbpool.close()
    def process_item(self,item,spider):
        self.dbpool.runInteraction(self.insert_db,item)

        return item

    def insert_db(self,tx,item):
        values=(
            item['asin'],
            item['title'],
            item['reviews'],
            item['rate'],
            item['page_num'],
            item['position_num'],
            item['price_initial'],
            item['price_true'],
            item['coupon'],
            item['sellername'],
        )
        sql='INSERT INTO '


