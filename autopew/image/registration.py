import numpy as np
from ..transform.affine import affine_from_AB, affine_transform
from ..gui.windows import image_point_registration
from .base import Image
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


class RegisteredImage(Image):
    def __init__(self, img, origin=None, rotate=0.0, flip=None):
        super().__init__(img)
        self.output_transform = None
        self.input_transform = None
        self.reference_pixels = None

    def transform_image_2D(self, transform):
        """
        Transform an image to match the shape and orientation of an image from the laser.
        """
        points = np.array(self.pixelcoords).reshape(-1, 2)
        coords = transform(points)
        return (*coords.T, self.image)

    def calibrate_input(self, inputpoints, pixelpoints):
        """
        Calibrate the transfrom external coordinates (e.g. TIMA xyz) to image pixel
        coordinates.
        """
        # this is an exercise of point-set registration
        self.input_transform = affine_transform(
            affine_from_AB(inputpoints, pixelpoints)
        )
        return self.input_transform

    def calibrate_output(self, pixelpoints, transformpoints):
        """
        Calibrate the transfrom from image pixel coordinates to external coordinates
        (i.e laser stage).
        """
        # this is an exercise of point-set registration
        self.output_transform = affine_transform(
            affine_from_AB(pixelpoints, transformpoints)
        )
        return self.output_transform

    def set_calibration_pixelpoints(self, pixelpoints=None, *args, **kwargs):
        if pixelpoints is None:  # load a gui
            self.reference_pixels = image_point_registration(
                self.image, *args, **kwargs
            )

        return self.reference_pixels
