import unittest
import time

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

    @mock.patch.object(WebanSpider, 'is_valid_response')
    @mock.patch.object(WebanSpider, 'retry')
    def test_parse_invalid(self, *args):
        self.spider.is_valid_response.return_value = False
        ret = mock.MagicMock()
        self.spider.retry.return_value = ret
        response = mock.MagicMock()
        expected = self.spider.parse(response)
        self.assertIn(ret, expected)

    def test_parse_detail_page(self):
        expected = self.spider.parse_detail_page(self.detail_page_response)
        self.assertIsInstance(expected, JobPostingItem)

    @mock.patch.object(WebanSpider, 'is_valid_response')
    @mock.patch.object(WebanSpider, 'retry')
    def test_parse_detail_page_invalid(self, *args):
        self.spider.is_valid_response.return_value = False
        ret = mock.MagicMock()
        self.spider.retry.return_value = ret
        response = mock.MagicMock()
        expected = self.spider.parse_detail_page(response)
        self.assertIs(ret, expected)

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

    @mock.patch('time.sleep')
    def test_retry(self, *args):
        url = 'http://example.com'
        request = Request(url=url)
        response = HtmlResponse(url=url, request=request)
        # retry returns Request with the same url for max_retry_times
        for i in range(WebanSpider.max_retry_times):
            request = self.spider.retry(response)
            time.sleep.assert_called_with(2)
            self.assertIsInstance(request, Request)
            self.assertEqual(request.url, url)
            response = HtmlResponse(url=url, request=request)
        # retry returns None after max_retry_times
        request = self.spider.retry(response)
        self.assertIsNone(request)
