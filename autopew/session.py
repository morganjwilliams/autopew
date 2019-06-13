import json
from pathlib import Path
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.image
import matplotlib.pyplot as plt
import logging
from .image.registration import RegisteredImage
from .util.readlase import ScanData

# from .targets import Point, Line, Map

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

class Stage(object):

    def __int__(self, limits=None):
        self.limits = limits

    def get_limits(self):
        return self.limits

# create stage <--> image transforms (2D), stage <--> stage transforms (3D)

class Session(object):
    """
    Session objects to store context for analytical sessions.
    """

    def __init__(self, report_template=None, stage=None):


        self.report_template = report_template
        self.registered_images = {}
        # self.priorities = None # Could prioritise points or lines etc
        self.points = pd.DataFrame()
        self.lines = pd.DataFrame()
        self.maps = pd.DataFrame()

        #self.stage = Stage()
        #self.stagelimits = self.stage.get_limits

    def load_image(self, name, image):
        self.registered_images[name] = RegisteredImage(image)
        return self.registered_images[name]

    def points_from_csv(
        self,
        filename,
        xvar="X",
        yvar="Y",
        zvar=None,
        labelvar=None,
        prependfile=True,
        image=None,
    ):
        """
        Add a set of points in pixel coordinates from a csv.
        """
        file = Path(filename)
        name = file.stem
        if zvar is None:  # just 2D
            vars = (xvar, yvar)
        else:
            vars = (xvar, yvar, zvar)

        df = pd.read_csv(filename)
        points = df.loc[:, vars]
        points.columns = points.columns.map(str.lower)

        if image is not None:  # if we need to transform coordinates
            if isinstance(image, RegisteredImage):
                if (
                    image not in self.registered_images.values()
                ):  # check if image loaded
                    image = self.load_image(name, image)
            else:
                image = self.load_image(name, image)

            points["image"] = name  # store the reference only

        self.points = pd.concat(
            [self.points, points], axis=0
        )  # point pixel coordinates
        return points

    def reorder_analyses(self):
        """
        Reorder analyses to be more efficient to minimise stage movement.
        """
        pass

    def standard_bracket(self, standard_name="Standard", interval=12):
        self.points
        return

    def autoflow(self, img, scancsv, newpoints):
        """
        Automated workflow given an image, a .scancsv with refernce points and a .csv
        with new points in it."""
        im = self.load_image(*img)

        points = self.points_from_csv(newpoints, image=im)
        scandata = ScanData(scancsv)
        refpoints = scandata.get_verticies()
        lasercoords = refpoints.loc[
            ("Spot" in i for i in refpoints.index.values), :
        ].values.astype(np.float)

        pc = im.set_calibration_pixelpoints()
        tfm = im.calibrate_output(pc, lasercoords[:, :-1])
        newverts = tfm(points.loc[:, ["x", "y"]].astype(np.float).values)
        return newverts

    def to_scancsv(self):
        """Create a .scancsv file."""
        pass

    def dump(self):
        """Dump configuration to json"""
        pass

    def report(self, template=None):
        pass


if __name__ == "__main__":
    pass
