import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..gui.base import screensize
from ..gui.windows import image_point_registration
from ..image import PewImage

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

"""
class PointSet(object):
    def __init__(self, points, coordinates=None):

        self.points = pd.DataFrame(points)
        self.points["coordinates"] = coordinates

    def __repr__(self):
        return self.points.__repr__()
"""


def pick_points(image_path, **kwargs):
    """
    Pick points on an image.
    """
    img = PewImage(image_path)
    return image_point_registration(img.image, **kwargs)
