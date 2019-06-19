from scipy import misc
import unittest
import matplotlib.pyplot as plt
from autopew.gui.windows import image_point_registration


class TestGUI(unittest.TestCase):
    def setUp(self):
        self.img = misc.face()

    def tearDown(self):
        plt.close("all")

    def test_gui_plot_window(self):
        ax = image_point_registration(self.img, timeout=10)  # 10 ms timeout


if __name__ == "__main__":
    unittest.main()
