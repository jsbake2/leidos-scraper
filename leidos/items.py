# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LeidosItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    location = scrapy.Field()
    applink = scrapy.Field()
    description = scrapy.Field()
    page_url = scrapy.Field()
    job_number = scrapy.Field()
    clearance_get = scrapy.Field()
    clearance_have = scrapy.Field()
    travel = scrapy.Field()
    job_category = scrapy.Field()
