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
    # 400 milliseconds delay (0.5 * 0.4 < delay < 1.5 * 0.4)
    download_delay = 0.4
    next_page_xpath = '//*[@id="pagerTopList"]//li[@class="paging_next"]/a/@href'
    detail_page_xpath = u'//*[@id="mainContents"]//a[img[@alt="詳細を見る"]]/@href'

    # TODO: http://stackoverflow.com/questions/28640102/retrying-a-scrapy-request-even-when-receiving-a-200-status-code
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
        item_loader.add_value('provider', self.name)
        item_loader.add_value('url', response.url)
        # TODO: parse detail page
        item_loader.add_xpath('description', u'//*[@id="mainContents"]//tr[th[.="仕事内容"]]/td/p')
        return item_loader.load_item()
