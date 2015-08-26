# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from datetime import datetime

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


class JobPostingItem(scrapy.Item):

    # re considerate this approach
    @staticmethod
    def _generate_id(urls):
        # TODO: generate id
        # self['id'] = 'ID'
        return urls

    id = scrapy.Field()
    provider = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        # output_processor=MapCompose(_generate_id, TakeFirst())
        output_processor=MapCompose(TakeFirst())
    )
    description = scrapy.Field(
        output_processor=TakeFirst()
    )
    created_at = scrapy.Field(
        output_processor=lambda: datetime.now()
    )
