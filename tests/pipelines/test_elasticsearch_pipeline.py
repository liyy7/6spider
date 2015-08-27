import unittest

from sixspider.pipelines import ElasticsearchPipeline


class TestElasticsearchPipeline(unittest.TestCase):
    def test_process_item(self):
        pipeline = ElasticsearchPipeline()
        processed_item = pipeline.process_item(None, None)
        self.assertIsNone(processed_item)
