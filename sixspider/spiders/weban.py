# -*- coding: utf-8 -*-
import scrapy


class WebanSpider(scrapy.Spider):
    name = 'weban'
    allowed_domains = ['weban.jp']
    start_urls = (
        'http://weban.jp/webapp/gen/list/itemSearchList?CMD=300&V5=1&V1=05&FID=300&A1=03&AX=1&V24=1&Z1=014&J1=12&J1=16&J1=03&J1=06&J1=08&J1=05&J1=01&J1=10&J1=04&J1=07&J1=14&J1=11&J1=02&J1=13&J1=15&J1=09',
    )

    def parse(self, response):
        pass
