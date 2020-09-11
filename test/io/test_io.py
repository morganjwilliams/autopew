import unittest
from autopew.io import PewIOSpecification


class TestGetHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_handler(self):
        handler = get_handler("mylasercoords.scancsv")
        self.assertIsInstance(handler, PewIOSpecification)
