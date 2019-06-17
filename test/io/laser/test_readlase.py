import unittest
from pathlib import Path
from autopew.util.meta import autopew_datafolder
from autopew.io.laser import readlase

test_lase = autopew_datafolder("examples") / "autopew_test.lase"
test_scancsv = autopew_datafolder("examples") / "autopew_test.scancsv"


class TestReadLase(unittest.TestCase):
    def setUp(self):
        self.file = test_lase

    def test_readlase(self):
        data = readlase.read_lasefile(self.file)


class TestReadScancsv(unittest.TestCase):
    def setUp(self):
        self.file = test_scancsv

    def test_readscancsv(self):
        data = readlase.read_scancsv(self.file)


class TestScanData(unittest.TestCase):

    def test_default(self):
        sd = readlase.ScanData(test_scancsv)

    def test_get_verticies(self):
        sd = readlase.ScanData(test_scancsv)
        verts = sd.get_verticies()


if __name__ == "__main__":
    unittest.main()
