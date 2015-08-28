import unittest
import inspect

from sixspider.spiders import weban


class ItemsTest(unittest.TestCase):
    def test(self):
        self.assertTrue(inspect.ismodule(weban))
