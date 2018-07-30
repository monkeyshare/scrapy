# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    asin = scrapy.Field()
    title = scrapy.Field()
    reviews = scrapy.Field()
    rate = scrapy.Field()
    page_num = scrapy.Field()
    position_num = scrapy.Field()
    price_initial = scrapy.Field()
    price_true = scrapy.Field()
    coupon = scrapy.Field()
    sellername = scrapy.Field()