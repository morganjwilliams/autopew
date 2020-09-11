import unittest
from autopew.io import PewIOSpecification, get_filehandler


class TestGetHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_filehandler(self):
        handler = get_filehandler("mylasercoords.scancsv")
        self.assertTrue(issubclass(handler, PewIOSpecification))
