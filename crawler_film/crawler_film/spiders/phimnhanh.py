__author__='toanqn'

import scrapy
from crawler_film.items import CrawlerFilmItem

class CrawlerFilm(scrapy.Spider):
    name = 'phimnhanh'
    allowed_domains = ['phimnhanh.com']
    start_urls = [
        'http://phimnhanh.com/phim-le'
    ]

    def parse(self, response):
        for selector in response.xpath('//li[@class="serial"]//a'):
            url = selector.xpath('./@href').extract_first('')
            yield scrapy.Request(url, callback=self.parse_detail)

        next_page = response.xpath('//li[@class="active"]/following::li/a/@href').extract_first()
        if(next_page):
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):

        item = CrawlerFilmItem()
        item['url'] = response.url

        item['title'] = response.xpath('//h1[@class="movie-title"]/text()').extract_first()

        item['image'] = response.xpath('//img[@class="photo"]/@src').extract_first()

        category = response.xpath('//p[contains(string(), "Thể loại:")]/span//text()').extract()
        item['category'] = "".join(str(tmp).strip() for tmp in category)

        item['quality'] = response.xpath('//span[@class="m-label q"]/text()').extract_first()

        item['type'] = response.xpath('//span[@class="m-label lang"]/text()').extract_first()

        item['year'] = response.xpath('//p[contains(string(), "Năm sản xuất:")]/span//text()').extract_first()

        item['description'] = response.xpath('//div[@class="entry entry-m"]/p/text()').extract_first()

        item['time'] = response.xpath('//span[@class="m-label ep"]/text()').extract_first()

        actors = response.xpath('//p[contains(string(), "Diễn viên:")]/span//text()').extract()
        item['actor'] = "".join(tmp for tmp in actors)

        item['country'] = response.xpath('//p[contains(string(), "Quốc gia:")]/span//text()').extract_first()

        imdb = response.xpath('//span[@class="m-label imdb"]/text()').extract_first()
        if(imdb):
            item['imdb'] = imdb[5:].strip()

        item['crawl_at'] = self.allowed_domains[0]

        return item
