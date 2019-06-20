import numpy as np
import matplotlib.image
from pathlib import Path
import PIL.Image
from ..util.plot import bin_edges_to_centres

PIL.Image.MAX_IMAGE_PIXELS = 1900000000


class PewImage(object):
    def __init__(self, img):
        self.load_imagearray(img)
        self.shape = self.image.size
        self.pixelcoords = np.meshgrid(
            *[bin_edges_to_centres(np.arange(s + 1)) for s in self.shape]
        )
        self.pixelbins = np.meshgrid(*[np.arange(s + 1) for s in self.shape])

    def load_imagearray(self, img):
        """Load an image and deal with formatting etc."""
        if isinstance(img, str) or isinstance(img, Path):
            self.image = PIL.Image.Image(img)  # .transpose(1, 0, 2)
        elif isinstance(img, self.__class__):
            self.image = img.image
        elif isinstance(img, np.ndarray):
            self.image = PIL.Image.fromarray(img)
        else:
            raise NotImplementedError

    def transform(self, A, size=None, resample=PIL.Image.NEAREST):
        """
        Transform the image via an affine transformation matrix using PIL.
        """
        size = size or self.im.size
        return self.image.transform(
            size,
            PIL.Image.AFFINE,
            data=np.linalg.inv(A)[:-1, :].flatten(),
            resample=resample,
        )

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
