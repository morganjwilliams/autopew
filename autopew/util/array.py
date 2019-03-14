import numpy as np
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def _pad(x):
    return np.hstack([x, np.ones((x.shape[0], 1))])


def _unpad(x):
    return x[:, :-1]
