import unittest
import inspect

from sixspider import pipelines


class PipelinesTest(unittest.TestCase):
    def test(self):
        self.assertTrue(inspect.ismodule(pipelines))
