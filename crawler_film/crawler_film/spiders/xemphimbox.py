__author__='toanqn'

import scrapy
import re
from crawler_film.items import CrawlerFilmItem

class CrawlerFilm(scrapy.Spider):
    name = 'xemphimbox'
    allowed_domains = ['xemphimbox.com']
    start_urls = [
        'http://xemphimbox.com/phim-le/'
    ]

    def parse(self, response):
        for selector in response.xpath('//div[@class="inner"]/a'):
            url = selector.xpath('./@href').extract_first('')
            yield scrapy.Request(url, callback=self.parse_detail)

        next_page = response.xpath('//span[@class="current"]/following::span[1]/a/@href').extract_first()
        if(next_page):
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):

        item = CrawlerFilmItem()
        item['url'] = response.url

        item['title'] = response.xpath('//h1[@class="name"]/span/text()').extract_first()

        url_img_raw = response.xpath('//div[@class="poster"]/img/@src').extract_first()
        url_imgs = re.match(r'.*&url=(.*)', url_img_raw, re.I)
        item['image'] = url_imgs.group(1)

        type = response.xpath('//dt[contains(string(), "Thể loại")]/following::dd[1]//text()').extract()
        item['type'] = "".join(str(tmp).strip() for tmp in type)

        item['quality'] = response.xpath('//span[@class="status"]/text()').extract_first()

        item['year'] = response.xpath('//dt[contains(string(), "Năm phát hành:")]/following::dd[1]//text()').extract_first()

        description = response.xpath('//div[@class="block-body"]/div/p/text()').extract()
        item['description'] = "".join(tmp for tmp in description)

        item['time'] = response.xpath('//dt[contains(string(), "Thời lượng:")]/following::dd[1]//text()').extract_first()

        actors = response.xpath('//dt[contains(string(), "Diễn viên:")]/following::dd[1]//text()').extract()
        item['actor'] = "".join(tmp for tmp in actors)

        item['view'] = response.xpath('//i[@class="micon views"]/following-sibling::span/text()').extract_first()

        item['country'] = response.xpath('//dt[contains(string(), "Quốc gia:")]/following::dd[1]//text()').extract_first()

        item['crawl_at'] = self.allowed_domains[0]

        return item
