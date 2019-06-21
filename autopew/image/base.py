import numpy as np
import matplotlib.image
from pathlib import Path
import PIL.Image
from ..transform.affine import affine_from_AB, affine_transform, zoom, translate
from ..util.plot import bin_edges_to_centres
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

PIL.Image.MAX_IMAGE_PIXELS = 1900000000


class PewImage(object):
    def __init__(self, img, extent=None):
        self.load_image(img)
        self.shape = self.image.size

        self.extent = extent
        if self.extent is None:
            self.extent = np.array([[0, 0], [*self.image.size]]).T.flatten()
        # should update these to use extent
        self.pixelcoords = np.meshgrid(
            *[bin_edges_to_centres(np.arange(s + 1)) for s in self.shape]
        )
        self.pixelbins = np.meshgrid(*[np.arange(s + 1) for s in self.shape])

    def load_image(self, img):
        """Load an image and deal with formatting etc."""
        if isinstance(img, str) or isinstance(img, Path):
            self.image = PIL.Image.open(img)  # .transpose(1, 0, 2)
        elif isinstance(img, PIL.Image.Image):
            self.image = img
        elif isinstance(img, self.__class__):
            self.image = img.image
        elif isinstance(img, np.ndarray):
            self.image = PIL.Image.fromarray(img)
        else:
            raise NotImplementedError

    def thumb(self, frac=0.05, resample=PIL.Image.BILINEAR):
        """
        Return a thumbnail downsampled version of the image.
        """
        size = np.ceil(frac * np.array(self.shape).flatten()).astype(int)
        return PewImage(self.image.resize(tuple(size), resample), extent=self.extent)

    def affine_extent(self, A):
        """
        Get the extent of the corners of the image (x0, x1, y0, y1) after an affine
        transform A.
        """
        tfm = affine_transform(A)
        x0, x1, y0, y1 = self.extent
        corners = np.array([[x0, y0], [x1, y0], [x1, y0], [x1, y1]])
        tcorners = tfm(corners)
        return np.array(
            [np.min(tcorners, axis=0), np.max(tcorners, axis=0)]
        ).T.flatten()

    def affine_transform(self, A, resample=PIL.Image.NEAREST):
        """
        Transform the image via an affine transformation matrix using PIL.
        """
        Z = zoom(*(1 / A.diagonal()[:-1]).flatten())  #  remove zoom from A
        M = Z @ A
        # get the size after affine transform, minus the zoom
        image = self.image.transform(
            self.image.size, # need to expand this due to shear/rotation effects
            PIL.Image.AFFINE,
            data=np.linalg.inv(M)[:-1, :].flatten(),
            resample=resample,
        )
        return image

    def maprgb(self):
        """
        Convert the image to RGB arrays.
        """
        img = np.asarray(self.image)
        shape = img.shape[:-1]
        c = img.reshape(-1, 3) / 255.0  # colors
        r, g, b = c.T
        r, g, b = (
            r.flatten().reshape(shape),
            g.flatten().reshape(shape),
            b.flatten().reshape(shape),
        )
        return r, g, b, c

    def __repr__(self):
        return ".".join(
            [str(i) for i in [self.__class__.__module__, self.__class__.__name__]]
        )

    def __str__(self):
        return "{}".format(self.__class__)
