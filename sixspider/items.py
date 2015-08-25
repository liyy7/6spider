# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class JobPostingItem(scrapy.Item):
    provider = scrapy.Field()
    description = scrapy.Field(
        output_processor=TakeFirst()
    )
