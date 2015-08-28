import unittest
import inspect

from sixspider import middlewares


class ItemsTest(unittest.TestCase):
    def test(self):
        self.assertTrue(inspect.ismodule(middlewares))
