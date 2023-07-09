from unittest import TestCase

from commons.helpers import copy_csv_to_table, truncate_table


class TestHelpers(TestCase):
    def setUp(self) -> None:
        self.table_name = "table-name"

    def test_copy_csv_to_table(self):
        actual = copy_csv_to_table(self.table_name, ["c1", "c2"], "/file-path")
        expected = (
            "copy table-name (c1, c2) from '/file-path'delimiter ','csv header"
        )
        self.assertEqual(actual, expected)

    def test_truncate_table(self):
        actual = truncate_table(self.table_name)
        expected = "truncate table-name"
        self.assertEqual(actual, expected)
