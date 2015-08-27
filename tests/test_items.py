import unittest
import inspect

from sixspider import items


class ItemsTest(unittest.TestCase):
    def test(self):
        self.assertTrue(inspect.ismodule(items))
