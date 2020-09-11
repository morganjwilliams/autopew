import unittest
from autopew.io import PewIOSpecification, get_filehandler


class TestGetHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_filehandler(self):
        handler = get_handler("mylasercoords.scancsv")
        self.assertIsInstance(get_filehandler, PewIOSpecification)
