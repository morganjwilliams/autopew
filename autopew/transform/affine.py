"""
Submodule for calculating affine transforms between planar coordinate systems.
"""
import sys
import logging
import numpy as np
from matplotlib.transforms import Affine2D

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


__RCOND__ = [-1, None][sys.version_info >= (3, 7)]  # 3.6 will fail with lapack error


def _pad(x):
    return np.hstack([x, np.ones((x.shape[0], 1))])


def _unpad(x):
    return x[:, :-1]


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
