import sys
import numpy as np
from matplotlib.transforms import Affine2D
from ..util.array import _pad, _unpad

__RCOND__ = [-1, None][sys.version_info >= (3, 7)] # 3.6 will fail with lapack error

def affine_from_AB(X, Y):
    A, res, rank, s = np.linalg.lstsq(_pad(X), _pad(Y), rcond=__RCOND__)
    return A


def transform_from_affine(A):
    return lambda x: _unpad(np.dot(_pad(x), A))
