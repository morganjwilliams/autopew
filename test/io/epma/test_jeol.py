import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from autopew.io.EPMA import JEOL
from autopew.util.general import remove_tempdir, temp_path
from autopew.util.meta import autopew_datafolder


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
