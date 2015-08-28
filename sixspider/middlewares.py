from scrapy.xlib.tx import ResponseFailed


class ValidateResponseDownloaderMiddleware(object):
    """
    This downloader middleware checks response by calling `spider.is_valid_response(response)`,
    If False returned, throw a `ResponseFailed` exception, otherwise do nothing.
    """

    def process_response(self, request, response, spider):
        if hasattr(spider, 'is_valid_response') and spider.is_valid_response(response) is False:
            raise ResponseFailed('invalid response')
        else:
            return response
