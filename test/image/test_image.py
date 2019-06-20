import unittest
from scipy import misc
import matplotlib.pyplot as plt
from autopew.image import PewImage


class TestPewImage(unittest.TestCase):
    def setUp(self):
        self.img = misc.face()

    def tearDown(self):
        plt.close("all")

    def test_image_load(self):
        im = PewImage(self.img)
        xi, yi = im.pixelcoords  # centres of pixels

    def test_image_imshow(self):
        im = PewImage(self.img)
        plt.imshow(im.image)

    def test_image_pcolormesh(self):
        im = PewImage(self.img)
        xi, yi = im.pixelcoords  # centres of pixels
        r, g, b, c = im.maprgb()
        im = plt.pcolormesh(xi, yi, r, color=c)
        im.set_array(None)


if __name__ == "__main__":
    unittest.main()
