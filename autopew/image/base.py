import numpy as np
import matplotlib.image
from pathlib import Path
from ..util.plot import bin_edges_to_centres


class Image(object):
    def __init__(self, img):
        self.load_imagearray(img)
        self.shape = self.image.shape[:-1]
        self.pixelcoords = np.meshgrid(
            *[bin_edges_to_centres(np.arange(s + 1)) for s in self.shape]
        )
        self.pixelbins = np.meshgrid(*[np.arange(s + 1) for s in self.shape])

    def load_imagearray(self, img):
        """Load an image and deal with formatting etc."""
        if isinstance(img, str) or isinstance(img, Path):
            im = matplotlib.image.imread(img)  # .transpose(1, 0, 2)
            self.image = im
        elif isinstance(img, self.__class__):
            self.image = img.image
        elif isinstance(img, np.ndarray):
            self.image = img
        else:
            raise NotImplementedError

    def __repr__(self):
        return ".".join(
            [str(i) for i in [self.__class__.__module__, self.__class__.__name__]]
        )

    def __str__(self):
        return "{}".format(self.__class__)
