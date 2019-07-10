import numpy as np
import matplotlib.image
from pathlib import Path
import PIL.Image
import PIL.ImageOps
from ..transform.affine import (
    affine_from_AB,
    affine_transform,
    zoom,
    translate,
    decompose_affine2d,
    compose_affine2d,
    corners,
)
from ..util.plot import bin_edges_to_centres
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

PIL.Image.MAX_IMAGE_PIXELS = 1900000000


def resize(im, size):
    new_im = PIL.Image.new("RGB", size)
    new_im.paste(im, (0, 0))
    return new_im


def pad(im, padding):
    if len(padding) == 1:
        padding = tuple(list(padding) * 4)
    if len(padding) == 2:
        padding = (padding[0], padding[0], padding[1], padding[1])
    return PIL.ImageOps.expand(im, padding)


def affine_extent(A, size, reversey=False):
    """
    Get the after an affine transform using matrix A from the bounds of the image
    of a specified size.

    [x0, y0] - [x1, y0]
       |     X    |
    [x0, y1] - [x1, y1]

    > [x0, x1, y0, y1]
    """
    tfm = affine_transform(A)
    crns = corners(size)
    tcrns = tfm(crns)
    extent = np.array([np.min(tcrns, axis=0), np.max(tcrns, axis=0)]).T.flatten()
    if reversey:
        extent = extent[[0, 1, 3, 2]]
    return extent


def extent_to_size(extent, type=int):
    """
    Calculate the size spanned by a given extent.
    """
    x0, x1, y0, y1 = extent
    size = np.ceil(np.abs([x1 - x0, y1 - y0]))
    return tuple(size.astype(type))


def affine_size(A, size, type=int):
    return extent_to_size(affine_extent(A, size), type=type)


class PewImage(object):
    def __init__(self, img, extent=None, transform=None):
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

        self.transform = transform

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

    def affine_transform(self, A, resample=PIL.Image.NEAREST, reversey=False):
        """
        Transform the image via an affine transformation matrix using PIL.
        """
        im = self.image
        centre = np.array(im.size) / 2
        cnrs = corners(im.size)
        C0 = translate(*-centre)  # translate image to origin
        C1 = translate(  # translate transformed image from origin
            *-np.min(affine_transform(A @ C0)(cnrs), axis=0)
        )
        T, Z, R = decompose_affine2d(A)
        AP = compose_affine2d(T, Z, R.T)  # rotation in opposite direction for PIL
        T = C1 @ AP @ C0  # Full affine matrix

        size = tuple(np.ceil(np.max(affine_transform(T)(cnrs), axis=0)).astype(int) + 1)
        extent = affine_extent(A, im.size, reversey=reversey)
        image = im.transform(
            size,  # need to expand this due to shear/rotation effects
            PIL.Image.AFFINE,
            data=np.linalg.inv(T)[:-1, :].flatten(),
            resample=PIL.Image.BILINEAR,
        )
        return PewImage(image, extent=extent, transform=A)

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
