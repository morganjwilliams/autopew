import numpy as np
import matplotlib.pyplot as plt
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def maprgb(img):
    c = img.reshape(-1, 3) / 255.0
    r, g, b = c.T
    r, g, b = (
        r.flatten().reshape(img.shape[:-1]),
        g.flatten().reshape(img.shape[:-1]),
        b.flatten().reshape(img.shape[:-1]),
    )
    return r, g, b, c
