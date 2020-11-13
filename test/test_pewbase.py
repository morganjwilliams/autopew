import numpy as np
import pandas as pd
from autopew.util.meta import autopew_datafolder
from autopew import Pew
from pathlib import Path
import unittest
from autopew.util.general import temp_path, remove_tempdir
from autopew.transform.affine import affine_transform, compose_affine2d, rotate

from itertools import product


def int_to_alpha(num):
    """
    Encode an integer (0-26) into alpha characters, useful for sequences of
    axes/figures.

    Parameters
    ----------
    int : :class:`int`
        Integer to encode.

    Returns
    -------
    :class:`str`
        Alpha-encoding of a small integer.

    """
    alphas = [chr(i).lower() for i in range(65, 65 + 26)]
    return alphas[num]


class TestPew(unittest.TestCase):
    def setUp(self):
        pdir = autopew_datafolder(subfolder="examples")
        self.temp = temp_path()
        self.infile, self.outfile = (
            pdir / "autopew_test.scancsv",
            self.temp / "autopew_test_exported.scancsv",
        )

        self.src_points = np.array([[0.0, 1.0], [1.1, 2], [2.0, 3.3], [2.11, 4.1]])
        self.dest_points = (
            affine_transform(compose_affine2d(R=rotate(30)))(self.src_points)
            + np.random.randn(*self.src_points.shape) * 0.01
        )

        self.srcpth, self.dstpath = self.temp / "src.csv", self.temp / "dest.csv"

        _src = pd.DataFrame(self.src_points, columns=["x", "y"])
        _src.insert(0, "name", pd.Series([int_to_alpha(x) for x in _src.index]))
        _src.to_csv(self.srcpth, index=False)

        _dst = pd.DataFrame(self.dest_points, columns=["x", "y"])
        _dst.insert(0, "name", pd.Series([int_to_alpha(x) for x in _dst.index]))
        _dst.to_csv(self.dstpath, index=False)

    def test_empty_instantiation(self):
        pew = Pew()

    def test_calibration_instantiation_methods(self):
        sources = [
            self.src_points.tolist(),
            self.src_points,
            pd.DataFrame(self.src_points),
            str(self.srcpth),
            self.srcpth,
        ]
        destinations = [
            self.dest_points.tolist(),
            self.dest_points,
            pd.DataFrame(self.dest_points),
            str(self.dstpath),
            self.dstpath,
        ]
        for src, dest in product(sources, destinations):
            with self.subTest(src=src, dest=dest):
                pew = Pew(src, dest)

    def test_load_samples(self):
        pass

    def test_export_samples(self):
        pass

    def test_export_samples_uncalibrated_error(self):
        pass

    def test_to_archive(self):
        pass

    def test_from_archive(self):
        pass

    def tearDown(self):
        remove_tempdir(self.temp)


# map = Pew().load_samples(infile).export_samples(outfile, enforce_transform=False)

if __name__ == "__main__":
    unittest.main()
