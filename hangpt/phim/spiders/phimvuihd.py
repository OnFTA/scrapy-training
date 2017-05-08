# !/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from phim.items import PhimItem
import hashlib
import datetime

class Phimvuihd(scrapy.Spider):
    name = "phimvuihd"
    allowed_domains = ["phimvuihd.net"]
    start_urls = "http://phimvuihd.net/phim-le/trang-"

    def start_requests(self):
        for index in range(1,9):
            url = self.start_urls + str(index) + ".html"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//div[@class="inner"]'):
            item = PhimItem()
            url = sel.xpath('./a[@class="poster"]/@href').extract_first('').strip()
            item['url'] = url
            print(url)
            new_url = url.encode('utf-8')
            item['url_sha1'] = hashlib.sha1(new_url).digest()
            item['title'] = sel.xpath('.//img/@alt').extract_first('').strip()
            item['image'] = sel.xpath('.//img/@src').extract_first('').strip()
            item['year'] =  sel.xpath('.//dfn[2]/text()').extract_first('').strip()
            quality = sel.xpath('./span[@class="status"]/text()').extract_first('').strip()
            quality_cut = quality.split("-")
            item['type'] = quality_cut[1]
            item['quality'] = quality_cut[0]
            request = scrapy.Request(url, callback=self.parse_data)
            request.meta['movie'] = item
            yield request

    def parse_data(self, response):
        item = response.meta['movie'].copy()
        item['category'] = response.xpath('string(//dd[2])').extract_first('').strip()
        item['actor'] = response.xpath('string(//dd[5])').extract_first('').strip()
        item['time'] = response.xpath('string(//dd[6])').extract_first('').strip()
        item['country'] = response.xpath('string(//dd[3])').extract_first('').strip()
        item['view'] = response.xpath('//div[@class="views"]//span/text()').extract_first('').strip()
        item['description'] = response.xpath('string(//div[@class="block-body"]//p)').extract_first('').strip()
        item['tags'] = response.xpath('string(//div[@class="block-body slider"])').extract_first('').strip()
        item['crawl_at'] = datetime.datetime.now()
        return item