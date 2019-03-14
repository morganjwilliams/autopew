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


def bin_centres_to_edges(centres):
    """
    Translates point estimates at the centres of bins to equivalent edges,
    for the case of evenly spaced bins.

    Todo
    ------
        * This can be updated to unevenly spaced bins, just need to calculate outer bins.
    """
    step = (centres[1] - centres[0]) / 2
    return np.append(centres - step, centres[-1] + step)


def bin_edges_to_centres(edges):
    """
    Translates edges of histogram bins to bin centres.
    """
    if edges.ndim == 1:
        steps = (edges[1:] - edges[:-1]) / 2
        return edges[:-1] + steps
    else:
        steps = (edges[1:, 1:] - edges[:-1, :-1]) / 2
        centres = edges[:-1, :-1] + steps
        return centres
