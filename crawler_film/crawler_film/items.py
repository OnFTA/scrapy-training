# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerFilmItem(scrapy.Item):
    url_sha1 = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    type = scrapy.Field()
    quality = scrapy.Field()
    year = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field()
    time = scrapy.Field()
    actor = scrapy.Field()
    imdb = scrapy.Field()
    view = scrapy.Field()
    country = scrapy.Field()
    crawl_at = scrapy.Field()
