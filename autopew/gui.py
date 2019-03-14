
import matplotlib.pyplot as plt
import numpy as np
import logging

from .util.gui import ZoomPan, add_timeout

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def image_registration(img, timeout=None):
    fig, ax = plt.subplots()

    def on_click(event):
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            ax.scatter(x, y, marker="D", s=50, zorder=2)
            ax.figure.canvas.draw()
        else:
            print("Clicked ouside axes bounds but inside plot window")

    fig.canvas.callbacks.connect("button_press_event", on_click)

    # figPan = zp.pan_factory(ax)
    zp = ZoomPan()
    scale = 1.1
    figZoom = zp.zoom_factory(ax, base_scale=scale)
    ax.imshow(img)
    if timeout is not None:
        add_timeout(fig, timeout)
        fig.timer.start()
        plt.show()
    return ax
