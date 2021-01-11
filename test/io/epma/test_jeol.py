import unittest
import numpy as np
import pandas as pd
from pathlib import Path
from autopew.util.general import temp_path, remove_tempdir
from autopew.util.meta import autopew_datafolder
from autopew.io.EPMA import JEOL


class TestWritePOS(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            data=[["A", 1, 2], ["B", 3, 14.8]], columns=["name", "x", "y"]
        )
        self.temp = temp_path()
        self.fp = self.temp / "exportedpoints.pos"

    def test_write_pos(self):
        df = JEOL.write_pos(self.df, filepath=self.fp, z=10.78)
        assert self.fp.exists()

    def tearDown(self):
        try:
            remove_tempdir(self.temp)
        except:
            pass


if __name__ == "__main__":
    unittest.main()
