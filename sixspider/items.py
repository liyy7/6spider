# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime
import hashlib

import scrapy
from scrapy.loader.processors import TakeFirst, Compose, Join


def _generate_id(values, loader_context):
    """hash `values` to generate and set `id` field"""
    item = loader_context['item']
    item['id'] = hashlib.sha1(''.join(str(v) for v in values)).hexdigest()
    return values


def _created_at_processor(values, loader_context):
    """accept datetime/int/float types as `created_at` field"""
    if values:
        first = values[0]
        if isinstance(first, datetime.datetime):
            return first
        elif isinstance(first, (int, float)):
            return datetime.datetime.fromtimestamp(first)
    item = loader_context['item']
    return item['created_at']


class JobPostingItem(scrapy.Item):
    id = scrapy.Field()
    created_at = scrapy.Field(output_processor=_created_at_processor)
    provider = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=Compose(_generate_id, TakeFirst()))
    description = scrapy.Field(output_processor=Join())
    work_term = scrapy.Field(output_processor=Join())
    work_hour = scrapy.Field(output_processor=Join())
    salary = scrapy.Field(output_processor=Join())
    holiday = scrapy.Field(output_processor=Join())
    treatment = scrapy.Field(output_processor=Join())
    work_place = scrapy.Field(output_processor=Join())
    application_qualification = scrapy.Field(output_processor=Join())
    application_method = scrapy.Field(output_processor=Join())
    application_side = scrapy.Field(output_processor=Join())
    application_tel = scrapy.Field(output_processor=Join())
    application_charge_person = scrapy.Field(output_processor=Join())
    company = scrapy.Field(output_processor=Join())
    company_service = scrapy.Field(output_processor=Join())
    company_location = scrapy.Field(output_processor=Join())
    company_url = scrapy.Field(output_processor=Join())

    def __init__(self):
        super(JobPostingItem, self).__init__(
            created_at=datetime.datetime.now())
