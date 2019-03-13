import numpy as np
from matplotlib.transforms import Affine2D


def _pad(x):
    return np.hstack([x, np.ones((x.shape[0], 1))])


def _unpad(x):
    return x[:, :-1]


def affine_from_AB(X, Y):
    A, res, rank, s = np.linalg.lstsq(_pad(X), _pad(Y), rcond=-1)
    return A


def transform_from_affine(A):
    return lambda x: _unpad(np.dot(_pad(x), A))
