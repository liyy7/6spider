# -*- coding: utf-8 -*-
import time

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
    # 100 ~ 300 milliseconds download delay (0.5 * 0.2 < delay < 1.5 * 0.2)
    download_delay = 0.2
    minimum_response_body_length = 20000
    max_retry_times = 3
    next_page_xpath = '//*[@id="pagerTopList"]//li[@class="paging_next"]/a/@href'
    detail_page_xpath = u'//*[@id="mainContents"]//a[img[@alt="詳細を見る"]]/@href'

    def retry(self, response):
        retries = response.request.meta.get('retry_times', 0) + 1
        if retries <= self.max_retry_times:
            # sleep 2 seconds before sending retry request
            time.sleep(2)
            self.logger.debug('Retrying %(request)s (failed %(retries)d times): %(body_length)s bytes',
                              {'request': response.request, 'retries': retries, 'body_length': len(response.body)})
            retryreq = response.request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority -= 1
            return retryreq
        else:
            self.logger.error('Gave up retrying %(request)s (failed %(retries)d times): %(body_length)s bytes',
                              {'request': response.request, 'retries': retries, 'body_length': len(response.body)})

    def is_valid_response(self, response):
        return len(response.body) >= self.minimum_response_body_length

    def parse(self, response):
        # validate response
        if not self.is_valid_response(response):
            yield self.retry(response)
        else:
            # find all detail pages
            for detail_page_url in response.xpath(self.detail_page_xpath).extract():
                yield scrapy.Request(response.urljoin(detail_page_url), callback=self.parse_detail_page)
            # find next page url
            next_page_url = response.xpath(self.next_page_xpath).extract_first()
            if next_page_url:
                yield scrapy.Request(response.urljoin(next_page_url))

    def parse_detail_page(self, response):
        # validate response
        if not self.is_valid_response(response):
            return self.retry(response)

        item_loader = ItemLoader(item=JobPostingItem(), response=response)
        item_loader.add_value('provider', self.name)
        item_loader.add_value('url', response.url)
        fields_dict = {
            'description': u'仕事内容',
            'work_term': u'勤務期間',
            'work_hour': u'勤務時間',
            'salary': u'給与',
            'holiday': u'休日・休暇',
            'treatment': u'待遇',
            'work_place': u'勤務地',
            'application_qualification': u'応募資格',
            'application_method': u'応募方法',
            'application_side': u'応募先',
            'application_tel': u'応募先電話番号',
            'application_charge_person': u'担当',
            'company': u'会社名',
            'company_service': u'事業内容',
            'company_location': u'所在地',
            'company_url': u'関連URL'
        }
        for field, keyword in fields_dict.items():
            item_loader.add_xpath(field, u'//*[@id="mainContents"]//tr[th[.="{}"]]/td/node()'.format(keyword))
        return item_loader.load_item()
