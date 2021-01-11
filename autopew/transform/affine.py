"""
Submodule for calculating affine transforms between planar coordinate systems.
"""
import sys
import logging
import numpy as np
from matplotlib.transforms import Affine2D
import scipy.linalg

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


__RCOND__ = [-1, None][sys.version_info >= (3, 7)]  # 3.6 will fail with lapack error


def _pad(x):
    x = np.array(x)
    return np.hstack([x, np.ones((x.shape[0], 1))])


def _unpad(x):
    x = np.array(x)
    return x[:, :-1]


def corners(size):
    x0, x1, y0, y1 = np.array([[0, 0], [*size]]).T.flatten()
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])


def affine_from_AB(X, Y):
    """
    Create an affine transforamtion matrix based on two sets of coordinates.

    note
    -----

        * This is an augmented matrix, and includes the translation component
    """
    X, Y = np.array(X), np.array(Y)
    if np.isclose(X, Y).all():
        return compose_affine2d()

    if not np.isfinite(X).all() and np.isfinite(Y).all():
        msg = "Inputs contain missing values; cannot construct affine matrix."
        raise AssertionError(msg)

    assert X.shape == Y.shape
    # least squares X * A = Y
    A, res, rank, s = np.linalg.lstsq(_pad(X), _pad(Y), rcond=__RCOND__)
    A[np.isclose(A, 0.0)] = 0.0
    return A.T


def affine_transform(A):
    """
    Create an affine transform function based on affine matrix A.

    Todo
    -----

        * Could refine this to accept scalars, lists etc
    """
    return lambda x: _unpad(np.dot(_pad(np.array(x)), A.T))


def translate(x=0, y=0):
    """
    Generate a 2D affine translation matrix.
    """
    T = np.eye(3)
    T[:-1, -1] = np.array([x, y])
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
    S[0, 1] = x
    S[1, 0] = y
    return S


def compose_affine2d(T=translate(0, 0), Z=zoom(1, 1), R=rotate(0)):
    """
    Compose an affine transformation matrix based on translation, zoom and rotation
    components.

    Parameters
    -----------
    T, Z, R : :class:`numpy.ndarray`
        Component affine transfrom matricies for translation, zoom/scaling and rotation.

    Returns
    ---------
    A : :class:`numpy.ndarray`
    """
    A = T @ Z @ R
    return A


def decompose_affine2d(A):
    """
    Decompose an affine transform into components using a polar transform.

    Returns
    --------
    T, Z, R : :class:`numpy.ndarray`

    Note
    -----

        This decomposes the transform into the sequence rotation - zoom - translation.

        To recompose this transform,
    """
    T = np.eye(3)
    T[:-1, -1] = A[:-1, -1]
    M = A.copy()
    M[:-1, -1] = 0.0
    R, Z = scipy.linalg.polar(M, side="left")
    for arr in [T, Z, R]:
        arr[np.isclose(arr, 0)] = 0.0
    return T, Z, R
