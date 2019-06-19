import unittest
import matplotlib.pyplot as plt
from autopew.workflow import pick_points
from scipy import misc


class TestPickPoints(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        plt.close("all")

    def test_default(self):
        pts = pick_points(misc.face(), timeout=10)


if __name__ == "__main__":
    unittest.main()
