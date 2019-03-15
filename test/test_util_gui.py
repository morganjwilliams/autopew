from scipy import misc
import unittest
import matplotlib.pyplot as plt
import autopew.util.gui as gui


#ax = gui.image_registration(misc.face(), timeout=10000)
#ax.figure.timer.stop()
#ax.figure.timer.start()


class TestGUI(unittest.TestCase):
    def setUp(self):
        self.img = misc.face()

    def test_gui_plot_window(self):
        ax = gui.image_point_registration(self.img, timeout=10000)


if __name__ == "__main__":
    unittest.main()
