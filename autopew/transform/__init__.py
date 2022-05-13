"""
Submodule for calculating and visualising affine transforms between planar
coordinate systems.
"""

import itertools
import logging

from .affine import affine_from_AB, affine_transform

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

__all__ = ["affine_from_AB", ", affine_transform"]
