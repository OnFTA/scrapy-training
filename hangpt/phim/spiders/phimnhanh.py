# !/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from phim.items import PhimItem
import hashlib
import datetime

class Phimvuihd(scrapy.Spider):
    name = "phimnhanh"
    allowed_domains = ["phimnhanh.com"]
    start_urls = "http://phimnhanh.com/phim-le?page="

    def start_requests(self):
        for index in range(1,518):
            url = self.start_urls + str(index)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//li[@class="serial"]'):
            item = PhimItem()
            url = sel.xpath('.//a/@href').extract_first('').strip()
            item['url'] = url
            new_url = url.encode('utf-8')
            item['url_sha1'] = hashlib.sha1(new_url).digest()
            item['title'] = sel.xpath('.//span[@class="title display"]/text()').extract_first('').strip()
            item['image'] = sel.xpath('.//span[@class="poster"]/img[2]/@src').extract_first('').strip()
            item['imdb'] = sel.xpath('.//span[@class="rate"]/text()').extract_first('').strip()
            item['time'] = sel.xpath('.//span[@class="m-label ep"]/text()').extract_first('').strip()
            item['type'] = sel.xpath('.//span[@class="m-label lang"]/text()').extract_first('').strip()
            item['quality'] = sel.xpath('.//span[@class="m-label q"]/text()').extract_first('').strip()
            request = scrapy.Request(url, callback=self.parse_data)
            request.meta['movie'] = item
            yield request

    def parse_data(self, response):
        item = response.meta['movie'].copy()
        item['year'] = response.xpath(
            'string(//div[@class="dt"]/p[8]/span)').extract_first('').strip()
        item['category'] = response.xpath('string(//div[@class="dt"]/p[5]/span)').extract_first('').strip()
        item['actor'] = response.xpath('string(//div[@class="dt"]/p[4]/span)').extract_first(
            '').strip()
        item['country'] = response.xpath('string(//div[@class="dt"]/p[6]/span)').extract_first('').strip()
        item['description'] = response.xpath('//div[@class="entry entry-m"]/p/text()').extract_first('').strip()
        item['crawl_at'] = datetime.datetime.now()
        return item