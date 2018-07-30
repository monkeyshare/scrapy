# -*- coding: utf-8 -*-
import scrapy

from amazon_crawl.items import AmazonListItem
import time
import random


class AmazonsSpider(scrapy.Spider):
    name = 'amazons'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/']
    def start_requests(self):
        url='https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=mattress+pad&rh=i%3Aaps%2Ck%3Amattress+pad'
        yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        next_page=response.xpath('//a[@id="pagnNextLink"]/@href').extract_first()
        page_num=response.xpath('//div[@id="pagn"]/span[@class="pagnCur"]/text()').extract_first()
        for result in response.xpath('//li[contains(@id,"result_")]'):
            item=AmazonListItem()
            asin=result.xpath('@data-asin').extract_first()
            position_num=result.xpath('@data-result-rank').extract_first()
            # title=result.xpath('div/div[4]/div[1]/a/h2/text()').extract_first()
            title=result.re_first('<h2[\w\W]+?>([\w\W]+?)</h2>')
            reviews=result.xpath('div/div[7]/a/text()').extract_first()
            rate=result.re_first('alt\">(.+?) out of 5')
            price_initial=result.xpath('div/div[5]/div/span[2]/text()').extract_first()
            reg='<a[\s\S]*<span class="a-offscreen">(.+?)</span>'
            price_true=result.re_first(reg)
            if result.re_first('with coupon'):
                coupon=True
            else:
                coupon=False
            sellername=result.re('<span class=\"a-size-small a-color-secondary\">(.+?)</span>')
            item['asin']=asin
            item['title']=title
            item['reviews']=reviews
            item['rate']=rate
            item['page_num']=page_num
            item['position_num']=position_num
            item['price_initial']=price_initial
            item['price_true']=price_true
            item['coupon']=coupon
            item['sellername']=sellername
            yield  item
        if next_page is not None:
            next_page=self.start_urls[0]+next_page
            time.sleep(random.uniform(3,6))
            yield scrapy.Request(next_page,self.parse)
        else:
            print(next_page)
            pass

