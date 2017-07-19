# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DungBeetleItem(scrapy.Item):
    species = scrapy.Field()
    genus = scrapy.Field()
    author = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    nomenclatural_type = scrapy.Field()
    licence = scrapy.Field()
    creator = scrapy.Field()

