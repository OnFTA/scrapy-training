# !/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from phim.items import PhimItem
import hashlib
import datetime

class Xemphimbox(scrapy.Spider):
    name = "phimbathu"
    allowed_domains = ["phimbathu.com"]
    start_urls = [
        "http://phimbathu.com/danh-sach/phim-le.html"
    ]


    def parse(self, response):
        if response.xpath('//li[@class="item no-margin-left"]'):
            for sel in response.xpath('//li[@class="item no-margin-left"]'):
                item = PhimItem()
                abs_url = sel.xpath('.//@href').extract_first('').strip()
                url = response.urljoin(abs_url)
                item['url'] = url
                print(url)
                new_url = url.encode('utf-8')
                item['url_sha1'] = hashlib.sha1(new_url).digest()
                item['title'] = sel.xpath('.//div/span/text()').extract_first('').strip()
                item['image'] = sel.xpath('.//@src').extract_first('').strip()
                request = scrapy.Request(url, callback=self.parse_data)
                request.meta['movie'] = item
                yield request
        if response.xpath('//div[@class="left-content"]//li[@class="item"]'):
            for sel in response.xpath('//div[@class="left-content"]//li[@class="item"]'):
                item = PhimItem()
                abs_url = sel.xpath('.//@href').extract_first('').strip()
                url = response.urljoin(abs_url)
                print(url)
                new_url = url.encode('utf-8')
                item['url_sha1'] = hashlib.sha1(new_url).digest()
                item['title'] = sel.xpath('.//div[1]/span/text()').extract_first('').strip()
                item['image'] = sel.xpath('.//@src').extract_first('').strip()
                request = scrapy.Request(url, callback=self.parse_data)
                request.meta['movie'] = item
                yield request

        next_page = response.xpath('//a[@class="navigation next"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, callback=self.parse)

    def parse_data(self, response):
        item = response.meta['movie'].copy()
        quality = response.xpath('string(//dt[contains(string(),"Đang phát:")]/following::dd[1])').extract_first('').strip()
        if "+" in quality:
            item['type'] = quality
        else:
            quality_cut = quality.split(' ')
            if len(quality_cut) > 1:
                item['quality'] = quality_cut[-1]
                item['type'] = quality_cut[0:-1]
            else:
                item['quality'] = quality
        item['year'] = response.xpath('string(//dt[contains(string(),"Năm xuất bản:")]/following::dd[1])').extract_first('').strip()
        item['category'] = response.xpath('string(//dt[contains(string(),"Thể loại:")]/following::dd[1])').extract_first('').strip()
        item['actor'] = response.xpath('string(//dt[contains(string(),"Diễn viên:")]/following::dd[1])').extract_first('').strip()
        item['time'] = response.xpath('string(//dt[contains(string(),"Thời lượng:")]/following::dd[1])').extract_first('').strip()
        item['country'] = response.xpath('string(//dt[contains(string(),"Quốc gia:")]/following::dd[1])').extract_first('').strip()
        item['view'] = response.xpath('string(//dt[contains(string(),"Lượt xem:")]/following::dd[1])').extract_first('').strip()
        item['imdb'] = response.xpath('//span[@class="average"]/text()').extract_first('').strip()
        item['tags'] = response.xpath('string(//div[@class="keywords"])').extract_first('').strip()
        item['description'] = response.xpath('string(//div[@class="tab"]/p)').extract_first('').strip()
        item['crawl_at'] = datetime.datetime.now()
        return item