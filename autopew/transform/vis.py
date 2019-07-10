import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches
import matplotlib.transforms
from .affine import affine_transform


def vis(A, ax=None):
    """
    Visualise the effect of an affine transfrom on a unit square.

    Parameters
    -------------
    A : :class:`numpy.ndarray`
        Affine matrix to visualise.
    ax : :class:`matplotlib.axes.Axes`, `None`
        Axes to plot on.

    Returns
    ---------
    :class:`matplotlib.axes.Axes`
    """
    p = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]])

    if ax is None:
        fig, ax = plt.subplots(1)

    c = matplotlib.patches.Ellipse(
        (0.5, 0.5), 1, 1, facecolor="None", edgecolor="k", alpha=0.5
    )

    ax.plot(*p.T, color="K", marker="s")
    ax.add_patch(c)
    ax.set_aspect("equal")

    T = affine_transform(A)
    ax.plot(*T(p).T, color="r", marker="s")

    transform = matplotlib.transforms.Affine2D()
    transform.set_matrix(A)
    c1 = matplotlib.patches.Ellipse(
        (0.5, 0.5), 1, 1, facecolor="None", edgecolor="r", alpha=0.5
    )
    c1.set_transform(transform + ax.transData)
    ax.add_patch(c1)

    return ax
