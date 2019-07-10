import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from ..transform.affine import affine_from_AB, affine_transform
import scipy.spatial
import scipy.interpolate
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def data_to_pixels_transform(ax):
    # convert pixels to axes
    a2p = ax.transData.transform
    d2a = ax.transAxes.transform

    return lambda x: a2p(d2a(x))


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


def plot_2dhull(data, ax=None, s=0, **plotkwargs):
    """
    Plots a 2D convex hull around an array of xy data points.
    """
    if ax is None:
        fig, ax = plt.subplots(1)
    chull = scipy.spatial.ConvexHull(data, incremental=True)
    x, y = data[chull.vertices].T
    lines = ax.plot(np.append(x, [x[0]]), np.append(y, [y[0]]), **plotkwargs)
    return lines


def plot_transform(
    src,
    dest=None,
    tfm=None,
    ref=None,
    ax=None,
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
    assert not ((dest is None) and (tfm is None))
    src = np.array(src)
    if dest is None:
        dest = tfm(src)
    else:
        tfm = affine_transform(affine_from_AB(src, dest))

    if ax is None:
        fig, ax = plt.subplots(1, 2, figsize=figsize, sharex=sharex, sharey=sharey)
    else:
        fig = ax[0].figure
    for a in ax:
        a.patch.set_alpha(0)

    for ix in range(src.shape[0]):
        con = ConnectionPatch(
            xyA=src[ix],
            xyB=dest[ix],
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
    ax[0].scatter(*src.T, marker="x", c="k", alpha=0.8)
    ax[1].scatter(*dest.T, marker="x", c="r", alpha=0.8)

    if ref is not None:
        s = fig.get_size_inches()[0] * 6.0
        ref = np.array(ref)
        tref = tfm(ref)
        for ix in range(ref.shape[0]):
            con = ConnectionPatch(
                xyA=ref[ix],
                xyB=tref[ix],
                coordsA="data",
                coordsB="data",
                axesA=ax[0],
                axesB=ax[1],
                color="k",
                zorder=5,
                ls="--",
                lw=0.5,
            )
            ax[0].add_artist(con)
        st = dict(edgecolors="k", facecolors="none", marker="o", s=s)
        ax[0].scatter(*ref.T, **st)
        ax[1].scatter(*tref.T, **st)

    if hull:
        _hull = src
        if ref is not None:  # incorporate the reference points here too
            _hull = np.vstack([_hull, ref])
        lines = plot_2dhull(_hull, ax=ax[0], color="k", ls="-", lw=0.5)
        ax[1].plot(*tfm(lines[0].get_path().vertices).T, color="k", ls="-", lw=0.5)

    ax[1].yaxis.tick_right()
    ax[1].yaxis.set_label_position("right")

    for b, lims, setr in zip(
        invert0 + invert1,
        [ax[0].get_xlim(), ax[0].get_ylim(), ax[1].get_xlim(), ax[1].get_ylim()],
        [ax[0].set_xlim, ax[0].set_ylim, ax[1].set_xlim, ax[1].set_ylim],
    ):
        if b & (lims[1] > lims[0]):
            setr(lims[::-1])
    plt.subplots_adjust(hspace=0.1)
    return fig
