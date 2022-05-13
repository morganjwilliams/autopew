import unittest

import matplotlib.pyplot as plt
from scipy import misc

from autopew.workflow import pick_points


class TestPickPoints(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        plt.close("all")

    def test_default(self):
        pts = pick_points(misc.face(), timeout=10)


if __name__ == "__main__":
    unittest.main()
