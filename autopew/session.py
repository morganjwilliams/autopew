from pathlib import Path
import numpy as np
import pandas as pd
from .transform.affine import affine_from_AB, affine_transform
from .image.registration import RegisteredImage
from .io.laser.readlase import ScanData
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def points_from_csv(
    filename,
    xvar="X",
    yvar="Y",
    zvar=None,
    labelvar=None,
    prependfile=True,
    encoding="cp1252",
):
    """
    Get a set of points in pixel coordinates from a ImageJ csv.
    """
    file = Path(filename)
    name = file.stem
    if zvar is None:  # just 2D
        vars = (xvar, yvar)
    else:
        vars = (xvar, yvar, zvar)

    points = pd.read_csv(filename, encoding=encoding)
    points = points.loc[:, vars]
    points.columns = points.columns.map(str.lower)
    return points


class Session(object):
    """
    Session objects to store context for analytical sessions.
    """

    def __init__(self, stage=None):
        self.registered_images = {}
        self.points = pd.DataFrame()
        self.lines = pd.DataFrame()
        self.maps = pd.DataFrame()

    def load_image(self, name, image):
        self.registered_images[name] = RegisteredImage(image)
        return self.registered_images[name]

    def load_points(self, points, image=None, **kwargs):
        """Load a set of points."""
        if isinstance(points, (str, Path)):
            points = points_from_csv(points, **kwargs)
        else:  # array, list
            points = pd.DataFrame(points)
            points.columns = ["x", "y"]

        self.points = pd.concat(
            [self.points, points], axis=0
        )  # point pixel coordinates

        if image is not None:  # if we need to transform coordinates
            if isinstance(image, RegisteredImage):
                if (
                    image not in self.registered_images.values()
                ):  # check if image loaded
                    image = self.load_image(name, image)
            else:
                image = self.load_image(name, image)

        return points

    def autoflow(self, img=None, src_coord=None, dest_coord=None, src_points=None):
        """
        Automated workflow given an image, a .scancsv with refernce points and a .csv
        with new points in it.

        Parameters
        -----------
        img
            Image to load.
        src_coord : :class:`numpy.ndarray`, :code:`None`
            Array of source coordinates (e.g. pixels for an image).
        dest_coord : :class:`str` | :class:`pathlib.Path`
            Path of scancsv with ordered reference points, or array of reference point
            coordinates.
        src_points : :class:`np.ndarray` | :class:`str` , :class:`pathlib.Path`
            Array or path of file with new set of points in source coordinates
            (e.g. pixels for an image).
        """

        if isinstance(dest_coord, (str, Path)):
            dest = ScanData(dest_coord).get_verticies()
            dest = dest.iloc[[("Spot" in i) for i in dest.index.values], :]
            dest = dest.loc[:, ["x", "y"]].values.astype(np.float)
        else:
            dest = np.array(dest_coord)

        logger.info("Dest Coords:\n{}".format(dest))

        if img is not None:
            logger.info("Loading Image.")
            im = self.load_image(*img)
            img = im

        if src_coord is None:  # Image is needed for picking in case of no src_coord
            src = im.set_calibration_pixelpoints()
            tfm = im.calibrate_output(src, dest)
        else:
            src = src_coord
            tfm = affine_transform(affine_from_AB(src, dest))

        logger.info("Source Coords:\n{}".format(src))

        newpoints = (
            self.load_points(src_points, image=img)
            .loc[:, ["x", "y"]]
            .astype(np.float)
            .values
        )
        logger.info("Calculating Dest Coords for new points.")
        return tfm(newpoints)

    def to_scancsv(self):
        """Create a .scancsv file."""
        pass

    def dump(self):
        """Dump configuration to json"""
        pass


if __name__ == "__main__":
    pass
