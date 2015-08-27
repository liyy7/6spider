import unittest
import inspect

from sixspider import settings


class SettingsTest(unittest.TestCase):
    def test(self):
        self.assertTrue(inspect.ismodule(settings))
