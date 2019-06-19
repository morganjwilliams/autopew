import unittest
from scipy import misc
import matplotlib.pyplot as plt
from autopew.image import registration as reg
from autopew.util.plot import maprgb


class TestRegisteredImage(unittest.TestCase):
    def setUp(self):
        self.img = misc.face()

    def tearDown(self):
        plt.close("all")

    def test_image_load(self):
        regim = reg.RegisteredImage(self.img)
        xi, yi = regim.pixelbins

    def test_image_imshow(self):
        regim = reg.RegisteredImage(self.img)
        xi, yi = regim.pixelbins
        r, g, b, c = maprgb(regim.image)
        plt.imshow(c.reshape(regim.image.shape))

    def test_image_pcolormesh(self):
        regim = reg.RegisteredImage(self.img)
        xi, yi = regim.pixelbins
        r, g, b, c = maprgb(regim.image)
        im = plt.pcolormesh(xi.T, yi.T, r, color=c)
        im.set_array(None)


if __name__ == "__main__":
    unittest.main()
