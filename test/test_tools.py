import unittest

from src.tools import Tools


class Unittest(unittest.TestCase):
    def setUp(self):
        self.tools = Tools()

    def test_get_utc_epoch(self):
        date = '13.04.2018 13:40'
        result = self.tools.get_utc_epoch(date)
        self.assertEqual(1523608800000, result)

    def test_get_utc_epoch_none(self):
        date = None
        result = self.tools.get_utc_epoch(date)
        self.assertIsNone(result)