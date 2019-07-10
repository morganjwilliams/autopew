import unittest
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
from autopew.image.base import PewImage, affine_extent, extent_to_size
from autopew.transform.affine import zoom, rotate, translate, shear, affine_transform

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

    def test_transforms_graphical(self):
        im = PewImage(self.img)
        A1, A2, A3 = zoom(1, 1.5), shear(0.3, 0), rotate(45)
        _im1 = im.affine_transform(A1)
        _im2 = im.affine_transform(A2)
        _im3 = im.affine_transform(A3)

        centre = np.array(im.image.size) / 2.0
        fig, ax = plt.subplots(2, 4, figsize=(12, 3), sharex=True, sharey=True)
        ax[0, 0].scatter(*centre, color="r")
        # get the max extent of images
        x0, x1, y0, y1 = 0, 1, 0, 1
        for ix, I in enumerate([im, _im1, _im2, _im3]):
            x0, x1, y0, y1 = (
                min(x0, np.min(I.extent[:2])),
                max(x1, np.max(I.extent[:2])),
                min(y0, np.min(I.extent[2:])),
                max(y1, np.max(I.extent[2:])),
            )
            ax[0, ix].imshow(I.image)
            ax[1, ix].imshow(I.image, extent=I.extent)

        size = np.max(im.image.size) * np.sqrt(2)
        ax = ax.flat

        for a in ax:
            a.set_aspect("equal")
            a.axis([x0, x1, y0, y1])


if __name__ == "__main__":
    unittest.main()
