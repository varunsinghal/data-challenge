from unittest import TestCase

from builder.base_builder import Pipeline


class TestPipeline(TestCase):
    def setUp(self) -> None:
        self.pipeline = Pipeline()

    def test_add(self):
        self.pipeline.add("query-1")
        self.assertEqual(len(self.pipeline._queries), 1)
