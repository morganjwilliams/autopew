import unittest
import matplotlib.pyplot as plt
from autopew.util.plot import *
from autopew.transform.affine import affine_from_AB, affine_transform


class TestPlotTransform(unittest.TestCase):
    def setUp(self):
        self.src = np.array([[5265.9, 199.4], [7978.7, 8284.4], [1812.1, 5060.5]])
        self.dest = np.array([[50416, 51960], [42049, 64332], [57833, 72297]])
        self.tfm = affine_transform(affine_from_AB(self.src, self.dest))

    def tearDown(self):
        plt.close("all")

    def test_default(self):
        fig = plot_transform(self.src, dest=self.dest)


if __name__ == "__main__":
    unittest.main()
