import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from ..transform.affine import affine_from_AB, affine_transform
from pyrolite.util.plot import plot_2dhull
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def data_to_pixels_transform(ax):
    # convert pixels to axes
    a2p = ax.transData.transform
    d2a = ax.transAxes.transform

    return lambda x: a2p(d2a(x))


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


def plot_transform(
    srcpoints,
    destpoints=None,
    tfm=None,
    refpoints=None,
    sharex=False,
    sharey=False,
    invert0=[False, False],
    invert1=[False, False],
    figsize=(10, 5),
    titles=["Source Coordinates", "Destination Coordinates"],
    hull=True,
):
    """
    Visualise an affine transfrom.
    """
    assert not destpoints is None and tfm is None
    if destpoints is None:
        destpoints = np.array(tfm(srcpoints))
    else:
        tfm = affine_transform(affine_from_AB(srcpoints, destpoints))

    srcpoints = np.array(srcpoints)
    fig, ax = plt.subplots(1, 2, figsize=figsize, sharex=sharex, sharey=sharey)
    for a in ax:
        a.patch.set_alpha(0)

    for ix in range(srcpoints.shape[0]):
        con = ConnectionPatch(
            xyA=srcpoints[ix],
            xyB=destpoints[ix],
            coordsA="data",
            coordsB="data",
            axesA=ax[0],
            axesB=ax[1],
            color="0.5",
            zorder=5,
            ls="--",
            lw=0.5,
        )
        ax[0].add_artist(con)

    ax[0].set_title(titles[0])
    ax[1].set_title(titles[1])
    ax[0].scatter(*srcpoints.T, marker="x", c="k", alpha=0.8)
    ax[1].scatter(*destpoints.T, marker="x", c="r", alpha=0.8)

    if refpoints is not None:
        s = fig.get_size_inches()[0] * 6.0
        refpoints = np.array(refpoints)
        st = dict(edgecolors="k", facecolors="none", marker="o", s=s)
        ax[0].scatter(*refpoints.T, **st)
        ax[1].scatter(*tfm(refpoints).T, **st)

    if hull:
        lines = plot_2dhull(
            srcpoints, ax=ax[0], splines=False, color="k", ls="-", lw=0.5
        )
        ax[1].plot(*tfm(lines[0].get_path().vertices).T, color="k", ls="-", lw=0.5)

    ax[1].yaxis.tick_right()
    ax[1].yaxis.set_label_position("right")

    for b, f in zip(
        invert0 + invert1,
        [
            ax[0].invert_xaxis,
            ax[0].invert_yaxis,
            ax[1].invert_xaxis,
            ax[1].invert_yaxis,
        ],
    ):
        if b:
            f()
    plt.subplots_adjust(hspace=0.1)
    plt.show()
    return fig
