import unittest

import vcr
import requests
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
from sixspider.spiders.weban import WebanSpider
from sixspider.items import JobPostingItem


def _get_response_from_url(url):
    return HtmlResponse(
        url=url,
        request=Request(url=url),
        body=requests.get(url).content)


class WebanSpiderTest(unittest.TestCase):
    @vcr.use_cassette()
    def test_parse(self):
        spider = WebanSpider()
        response = _get_response_from_url(spider.start_urls[0])

        got_requests = list(spider.parse(response))
        for request in got_requests:
            self.assertIsInstance(request, Request)

        next_page_requests = list(r for r in got_requests if r.callback is None)
        self.assertEqual(len(next_page_requests), 1)

        detail_page_requests = list(r for r in got_requests if r.callback == spider.parse_detail_page)
        self.assertEqual(len(detail_page_requests), 50)

    @vcr.use_cassette()
    def test_parse_detail_page(self):
        spider = WebanSpider()
        response = _get_response_from_url(spider.start_urls[0])
        detail_page_request = list(r for r in spider.parse(response) if r.callback == spider.parse_detail_page)[0]
        detail_page_response = _get_response_from_url(detail_page_request.url)

        got_item = spider.parse_detail_page(detail_page_response)
        self.assertIsInstance(got_item, JobPostingItem)
