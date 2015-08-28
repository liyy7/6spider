import unittest

import mock
from scrapy.http import Request, Response
from scrapy.xlib.tx import ResponseFailed

from sixspider.middlewares import ValidateResponseDownloaderMiddleware


class TestValidateResponseDownloaderMiddleware(unittest.TestCase):
    def setUp(self):
        self.downloader_middleware = ValidateResponseDownloaderMiddleware()
        self.spider = mock.MagicMock()
        self.request = Request(url='http://example.com')
        self.response = Response(url='http://example.com', request=self.request)

    def test_process_response_without_validate_method(self):
        expected = self.downloader_middleware.process_response(self.request, self.response, self.spider)
        self.assertIs(expected, self.response)

    def test_process_response_with_validate_method(self):
        self.spider.is_valid_response.return_value = True
        expected = self.downloader_middleware.process_response(self.request, self.response, self.spider)
        self.spider.is_valid_response.assert_called_with(self.response)
        self.assertIs(expected, self.response)

    def test_process_response_raise_exception(self):
        self.spider.is_valid_response.return_value = False
        with self.assertRaises(ResponseFailed):
            self.downloader_middleware.process_response(self.request, self.response, self.spider)
        self.spider.is_valid_response.assert_called_with(self.response)
