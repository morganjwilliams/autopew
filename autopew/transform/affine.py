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
    x = np.array(x)
    return np.hstack([x, np.ones((x.shape[0], 1))])


def _unpad(x):
    x = np.array(x)
    return x[:, :-1]


def affine_from_AB(X, Y):
    """
    Create an affine transforamtion matrix based on two sets of coordinates.

    note
    -----

        * This is an augmented matrix, and includes the translation component
    """
    X, Y = np.array(X), np.array(Y)
    assert X.shape == Y.shape
    # least squares X * A = Y
    A, res, rank, s = np.linalg.lstsq(_pad(X), _pad(Y), rcond=__RCOND__)
    A[np.isclose(A, 0.0)] = 0.0
    return A


def affine_transform(A):
    """
    Create an affine transform function based on affine matrix A.

    Todo
    -----

        * Could refine this to accept scalars, lists etc
    """
    return lambda x: _unpad(np.dot(_pad(np.array(x)), A))


def translate(xy=[0, 0]):
    """
    Generate a 2D affine translation matrix.
    """
    T = np.eye(3)
    T[-1, :-1] = np.array(xy)
    return T


def rotate(theta=0, degrees=True):
    """
    Generate a 2D affine rotation matrix.

    Uses clockwise rotations.
    """
    θ = np.deg2rad(theta)
    R = np.eye(3)
    R[[0, 1], [0, 1]] = np.cos(θ)
    R[[1, 0], [0, 1]] = -np.sin(θ), np.sin(θ)
    return R


def zoom(x=1, y=1):
    """
    Generate a 2D affine zoom matrix.
    """
    Z = np.eye(3)
    Z[0, 0] = x
    Z[1, 1] = y
    return Z


def shear(x=0, y=0):
    """
    Generate a 2D affine shear matrix.
    """
    S = np.eye(3)
    S[0, 1] = y
    S[1, 0] = x
    return S
