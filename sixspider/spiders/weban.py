# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from sixspider.items import JobPostingItem


class WebanSpider(scrapy.Spider):
    name = 'weban'
    allowed_domains = ['weban.jp']
    start_urls = (
        'http://weban.jp/webapp/gen/list/itemSearchList/'
        '?CMD=300&FID=300&A1=03&AX=1&V1=05&V2=1&V13=40&Z1=014&V3=50&V5=1&V24=0',
    )
    next_page_xpath = '//div[@id="pagerTopList"]//li[@class="paging_next"]/a/@href'
    # TODO
    detail_page_xpath = ''

    def parse(self, response):
        # find all detail pages
        for detail_page_url in response.xpath(self.detail_page_xpath).extract():
            yield scrapy.Request(response.urljoin(detail_page_url), callback=self.parse_detail_page)
        # find next page url
        next_page_url = response.xpath(self.next_page_xpath).extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_detail_page(self, response):
        item_loader = ItemLoader(item=JobPostingItem(), response=response)
        # TODO: parse detail page
        # ...
        return item_loader.load_item()
