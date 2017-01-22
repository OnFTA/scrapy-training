__author__ = 'toanqn'

import scrapy
from crawler_film.items import CrawlerFilmItem

class PhimBatHu(scrapy.Spider):

    name = 'phimbathu'
    allowed_domains = ['phimbathu.com']
    start_urls = [
        "http://phimbathu.com/danh-sach/phim-le.html"
    ]

    def parse(self, response):
        for selector in response.xpath('//li[@class="item" or @class="item no-margin-left"]/a'):
            abs_url = selector.xpath('./@href').extract_first()
            url = response.urljoin(abs_url)
            yield scrapy.Request(url, callback=self.parse_detail)

        next_page = response.xpath('//li/a[@class="current"]/following::li[1]/a/@href').extract_first()
        if (next_page):
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):

        item = CrawlerFilmItem()

        item['url'] = response.url

        item['title'] = response.xpath('//p[@class="title"]/text()').extract_first()

        item['image'] = response.xpath('//img[@itemprop="image"]/@src').extract_first()

        type = response.xpath('//dt[contains(string(), "Thể loại")]/following::dd[1]//text()').extract()
        item['type'] = "".join(str(tmp).strip() for tmp in type)

        item['quality'] = response.xpath('//dt[contains(string(), "Đang phát:")]/following::dd[1]/text()').extract_first()

        item['year'] = response.xpath(
            '//dt[contains(string(), "Năm xuất bản:")]/following::dd[1]/text()').extract_first()

        description = response.xpath('//div[@id="info-film"]//text()').extract()
        item['description'] = "".join(tmp for tmp in description)

        item['time'] = response.xpath(
            '//dt[contains(string(), "Thời lượng:")]/following::dd[1]/text()').extract_first()

        actors = response.xpath('//dt[contains(string(), "Diễn viên:")]/following::dd[1]//text()').extract()
        item['actor'] = "".join(tmp for tmp in actors)

        item['view'] = response.xpath('//dt[contains(string(), "Lượt xem:")]/following::dd[1]/text()').extract_first()

        item['tags'] = response.xpath('//div[@class="keywords"]//text()').extract_first()

        item['country'] = response.xpath(
            '//dt[contains(string(), "Quốc gia:")]/following::dd[1]//text()').extract_first()

        item['crawl_at'] = self.allowed_domains[0]

        return item