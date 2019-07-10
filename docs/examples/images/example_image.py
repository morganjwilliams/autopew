import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from pathlib import Path

np.random.seed(82)
fig, ax = plt.subplots(1)
im = misc.face()
ax.axis("off")
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
data = np.random.rand(50, 2)
refpoints = np.array([[0.01, 0.05], [0.98, 0.9], [0.1, 0.9], [0.75, 0.03]])
ax.scatter(
    *refpoints.T,
    facecolors="r",
    edgecolors="r",
    marker="+",
    s=50,
    zorder=5,
    label="Reference Points"
)
for ix, (x, y) in enumerate(refpoints):
    ax.annotate(
        "R{:d}".format(ix + 1),
        xy=(0.5 + (x - 0.5) * 0.95, 0.5 + (y - 0.5) * 0.95),
        xytext=(0.5 + (x - 0.5) * 0.5, 0.5 + (y - 0.5) * 0.5),
        ha=["left", "right"][(x - 0.5) > 0],
        va=["bottom", "top"][(y - 0.5) > 0],
        fontsize=14,
        weight="bold",
        arrowprops=dict(facecolor="none", lw=1, arrowstyle="wedge,tail_width=0.5"),
    )

ax.scatter(*data.T, marker="x", facecolor="0.2", label="Sample Points")
ax.imshow(im, extent=(0, 1, 0, 1), alpha=0.5)
ax.plot(*np.array([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]).T, color="k", lw=2)
ax.set_aspect(im.shape[0] / im.shape[1])
ax.axis((0, 1.0, 0, 1.0))
ax.legend(
    bbox_to_anchor=(0.5, 1.01),
    loc="lower center",
    frameon=False,
    facecolor=None,
    ncol=2,
)
fig.savefig(Path("../../source/_static/img.jpg"), dpi=300)
