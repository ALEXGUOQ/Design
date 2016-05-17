# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DesignItem(scrapy.Item):
    title = scrapy.Field()
    icon = scrapy.Field()
    img = scrapy.Field()
    tags = scrapy.Field()

class IconItem(scrapy.Item):
    icon = scrapy.Field()
    tags = scrapy.Field()

class Photography(scrapy.Item):
    icon = scrapy.Field()