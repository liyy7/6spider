import datetime
import hashlib
import unittest

import mock
from scrapy.loader import ItemLoader
from sixspider.items import JobPostingItem

datetime.datetime = type('MockDatetime', (datetime.datetime,), {})


class JobPostingItemTest(unittest.TestCase):
    @mock.patch('datetime.datetime.now')
    def test_init(self, *_):
        mocked_now = datetime.datetime(2015, 8, 27, 20, 21, 58, 25717)
        datetime.datetime.now.return_value = mocked_now

        item = JobPostingItem()
        self.assertEqual(item['created_at'], mocked_now)

    def test_fields(self):
        item = JobPostingItem()
        self.assertSetEqual(set(item.fields), set('url created_at provider id description'.split(' ')))

    @mock.patch('hashlib.sha1')
    def test_id_field(self, *_):
        mocked_id = 'foo'
        hashlib.sha1.return_value.hexdigest.return_value = mocked_id

        item_loader = ItemLoader(JobPostingItem())
        item = item_loader.load_item()
        self.assertNotIn('id', item)
        item_loader.add_value('url', 'http://example.com')
        item = item_loader.load_item()
        self.assertEqual(item['id'], mocked_id)

    @mock.patch('datetime.datetime.now')
    def test_created_at_filed(self, *_):
        mocked_now = datetime.datetime(2015, 8, 27, 20, 21, 58, 25717)
        datetime.datetime.now.return_value = mocked_now

        # fill with now if non-timestamp value passed
        item_loader = ItemLoader(JobPostingItem())
        item_loader.add_value('created_at', "foo")
        item = item_loader.load_item()
        self.assertEqual(item['created_at'], mocked_now)

        # fill with passed datetime
        dt = datetime.datetime(2015, 8, 27, 20, 21, 58, 25717)

        item_loader = ItemLoader(JobPostingItem())
        item_loader.add_value('created_at', dt)
        item = item_loader.load_item()
        self.assertEqual(item['created_at'], dt)

        # fill with passed float timestamp
        timestamp = 1440674518.025717
        dt = datetime.datetime(2015, 8, 27, 20, 21, 58, 25717)

        item_loader = ItemLoader(JobPostingItem())
        item_loader.add_value('created_at', timestamp)
        item = item_loader.load_item()
        self.assertEqual(item['created_at'], dt)

        # fill with passed int timestamp
        timestamp = 1440674518
        dt = datetime.datetime(2015, 8, 27, 20, 21, 58)

        item_loader = ItemLoader(JobPostingItem())
        item_loader.add_value('created_at', timestamp)
        item = item_loader.load_item()
        self.assertEqual(item['created_at'], dt)
