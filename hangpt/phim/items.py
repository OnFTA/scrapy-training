# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PhimItem(scrapy.Item):
    # define the fields for your item here like:
    #  url_sha1,title,url,image,type,quality,year,category,tags,description,time,actor,imdb,view,country,crawl_at
    url_sha1 = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    type = scrapy.Field() #thuyet minh hay Vietsub
    quality = scrapy.Field() #HD
    year = scrapy.Field()
    category = scrapy.Field() #loai
    tags = scrapy.Field()
    description = scrapy.Field()
    time = scrapy.Field()
    actor = scrapy.Field()
    imdb = scrapy.Field()
    view = scrapy.Field()
    country = scrapy.Field()
    crawl_at = scrapy.Field()
    pass
