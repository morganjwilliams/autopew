import sys
import logging
import numpy as np
from matplotlib.transforms import Affine2D
from ..util.array import _pad, _unpad

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


__RCOND__ = [-1, None][sys.version_info >= (3, 7)]  # 3.6 will fail with lapack error


def affine_from_AB(X, Y):
    A, res, rank, s = np.linalg.lstsq(_pad(X), _pad(Y), rcond=__RCOND__)
    return A


def transform_from_affine(A):
    return lambda x: _unpad(np.dot(_pad(x), A))


def inverse_transform_from_affine(A):
    return lambda x: _unpad(np.dot(_pad(x), np.linalg.inv(A)))
