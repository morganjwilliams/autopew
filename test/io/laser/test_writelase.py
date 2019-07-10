import unittest
import numpy as np
from autopew.io.laser import writelase


class TestXY2Scancsv(unittest.TestCase):
    def setUp(self):
        self.xy = np.array([[0, 1], [1, 0]])

    def test_xy2scansv(self):
        df = writelase.xy2scansv(self.xy)


if __name__ == "__main__":
    unittest.main()
