import matplotlib.pyplot as plt
from IPython import get_ipython
from .base import *


def image_point_registration(img, timeout=None):
    """
    Launches a window which can be clicked to add points.
    """
    ipython = get_ipython()
    if ipython is not None:
        ipython.run_line_magic("matplotlib", "qt")
    plt.ion()  # interactive mode - won't close plots.
    fig, ax = plt.subplots()
    points = []

    def on_click(event):
        if event.button == 1:
            if event.inaxes is not None:
                x, y = event.xdata, event.ydata
                ax.scatter(x, y, marker="D", s=50, zorder=2)
                ax.figure.canvas.draw()
                points.append([x, y])
            else:
                print("Clicked ouside axes bounds but inside plot window")

    fig.canvas.callbacks.connect("button_press_event", on_click)

    zp = ZoomPan()
    scale = 1.1
    figZoom = zp.zoom_factory(ax, base_scale=scale)
    figPan = zp.pan_factory(ax)
    ax.imshow(img, origin="upper")
    if timeout is not None:
        Timeout(fig, timeout)
        fig.timer.start()
    if hasattr(fig, "timer"):
        fig.canvas.mpl_connect("scroll_event", fig.timer.reset)

    position_figure(fig)
    plt.show(block=True)  # will be alive until close
    plt.ioff()  # turn interactive mode off, other plots won't be kept alive
    if ipython is not None:
        ipython.run_line_magic("matplotlib", "inline")
    return np.array(points)
