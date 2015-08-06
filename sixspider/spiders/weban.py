# -*- coding: utf-8 -*-
import scrapy


class WebanSpider(scrapy.Spider):
    name = "weban"
    allowed_domains = ["weban.jp"]
    start_urls = (
        'http://www.weban.jp/',
    )

    def parse(self, response):
        pass
