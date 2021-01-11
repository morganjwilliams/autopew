import unittest
import numpy as np
import pandas as pd
from pathlib import Path
from autopew.util.general import temp_path, remove_tempdir
from autopew.util.meta import autopew_datafolder
from autopew.io.laser import chromium

test_lase = autopew_datafolder("examples") / "autopew_test.lase"
test_scancsv = autopew_datafolder("examples") / "autopew_test.scancsv"


class TestReadScancsv(unittest.TestCase):
    def setUp(self):
        self.file = test_scancsv

    def test_readscancsv(self):
        df = chromium.read_scancsv(self.file)


class TestWriteScancsv(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(np.array([[0, 1], [1, 0]]), columns=["x", "y"])
        self.df["name"] = ["A", "B"]
        self.fp = temp_path() / "exportedpoints.csv"

    def test_write_scancsv(self):
        df = chromium.write_scancsv(self.df, filepath=self.fp)

    def tearDown(self):
        try:
            remove_tempdir(self.fp)
        except:
            pass


class TestReadLase(unittest.TestCase):
    def setUp(self):
        self.file = test_lase

    def test_readlase(self):
        df = chromium.read_lasefile(self.file)


if __name__ == "__main__":
    unittest.main()
