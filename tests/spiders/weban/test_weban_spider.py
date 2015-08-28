import unittest

import mock
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
    def setUp(self):
        self.spider = WebanSpider()
        start_response = _get_response_from_url(self.spider.start_urls[0])
        start_requests = list(self.spider.parse(start_response))
        self.next_page_requests = list(r for r in start_requests if r.callback is None)
        self.detail_page_requests = list(r for r in start_requests if r.callback == self.spider.parse_detail_page)
        self.detail_page_response = _get_response_from_url(self.detail_page_requests[0].url)

    def test_parse(self):
        self.assertEqual(len(self.next_page_requests), 1)
        self.assertEqual(len(self.detail_page_requests), 50)
        for request in self.next_page_requests + self.detail_page_requests:
            self.assertIsInstance(request, Request)

    def test_parse_detail_page(self):
        expected = self.spider.parse_detail_page(self.detail_page_response)
        self.assertIsInstance(expected, JobPostingItem)

    def test_is_valid_response(self):
        response = mock.MagicMock()

        response.body.__len__.return_value = 0
        expected = self.spider.is_valid_response(response)
        self.assertFalse(expected)

        response.body.__len__.return_value = 20000
        expected = self.spider.is_valid_response(response)
        self.assertTrue(expected)

        response.body.__len__.return_value = 40000
        expected = self.spider.is_valid_response(response)
        self.assertTrue(expected)
