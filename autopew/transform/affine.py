"""
Submodule for calculating affine transforms between planar coordinate systems.
"""
import sys
import logging
import numpy as np
from matplotlib.transforms import Affine2D
from ..util.array import _pad, _unpad

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


__RCOND__ = [-1, None][sys.version_info >= (3, 7)]  # 3.6 will fail with lapack error


def affine_from_AB(X, Y):
    """
    Create an affine transform matrix based on two sets of coordinates.
    """
    assert X.shape == Y.shape
    A, res, rank, s = np.linalg.lstsq(_pad(X), _pad(Y), rcond=__RCOND__)
    return A


def affine_transform(A):
    """
    Create an affine transform function based on affine matrix A.
    """
    return lambda x: _unpad(np.dot(_pad(x), A))
