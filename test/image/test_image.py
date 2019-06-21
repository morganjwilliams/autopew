import unittest
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
from autopew.image import PewImage
from autopew.transform.affine import zoom, rotate, translate, shear, affine_transform
import PIL.Image


class TestPewImage(unittest.TestCase):
    def setUp(self):
        # default image
        self.img = misc.face()

    def tearDown(self):
        plt.close("all")

    def test_load_array(self):
        image = PewImage(self.img)

    def test_load_PIL_Image(self):
        pass

    def test_load_PEWImage(self):
        pass

    def test_load_strpath(self):
        pass

    def test_load_pathlibpath(self):
        pass

    def test_extent(self):
        im = PewImage(self.img)
        thumb = im.thumb()
        arraysize = self.img.shape
        imextent = im.extent
        thumbextent = thumb.extent
        # could add test for original image extent
        self.assertTrue(np.allclose(imextent, thumbextent))

    def test_thumb(self):
        im = PewImage(self.img)
        thumb = im.thumb()
        self.assertTrue(thumb.image.size < im.image.size)

    def test_affine_extent(self):
        im = PewImage(self.img)
        thumb = im.thumb()
        Z = zoom(2, 2)
        imextent = im.extent
        aextent = affine_extent(Z, size=im.image.size)
        self.assertTrue((np.abs(aextent) >= np.abs(imextent)).all())

    def test_affine_transform(self):
        im = PewImage(self.img)
        affine_im = im.affine_transform(rotate(30))
        # check for clockwise rotation

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
