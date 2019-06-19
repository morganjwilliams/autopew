import numpy as np
import tkinter as tk
import matplotlib
from matplotlib.backend_bases import TimerBase
from ..util.plot import *
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def position_figure(fig, pos=None, size=None, scale=0.9, offset=0.05):
    """
    Rescale and position a figure window.
    """
    backend = matplotlib.get_backend()
    mgr = fig.canvas.manager
    if backend == "TkAgg":
        size = size or scale * np.array(mgr.window.maxsize())
        pos = pos or offset * size
        mgr.resize(*size)
        mgr.window.wm_geometry("+{:d}+{:d}".format(*[int(i) for i in pos]))
    elif backend == "WXAgg":  # need to find a way to set size
        # size = scale * mgr.window.maxsize()
        # pos = pos or offset * size
        size = size or scale * screensize()
        mgr.window.SetPosition(pos)
    else:  # QT and GTK
        size = size or scale * screensize()
        pos = pos or offset * size
        mgr.window.setGeometry(*pos, *size)


def screensize():
    """
    Get the screen size in pixels.
    """
    root = tk.Tk()
    return np.array([root.winfo_screenwidth(), root.winfo_screenheight()])


def timer_reset(self, *args, **kwargs):
    """
    Timer reset for TimerQT objects.
    """
    self._timer.stop()
    self._timer.setInterval(self._interval)
    logger.info("Timer Reset: ")
    self._timer.start()


setattr(TimerBase, "reset", timer_reset)


def Timeout(fig, timeout=1000):
    timer = fig.canvas.new_timer(interval=timeout)
    timer.add_callback(close_event)
    fig.timer = timer
    fig.canvas.callbacks.connect("button_press_event", timer.reset)


def close_event():
    plt.close()  # timer calls this function after 3 seconds and closes the window


class ZoomPan(object):
    """https://stackoverflow.com/a/19829987"""

    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

    def zoom_factory(self, ax, base_scale=2.0):
        def zoom(event):
            """This function zooms the image upon scrolling the mouse wheel.
            Scrolling it in the plot zooms the plot. Scrolling above or below the
            plot scrolls the x axis. Scrolling to the left or the right of the plot
            scrolls the y axis. Where it is ambiguous nothing happens.
            NOTE: If expanding figure to subplots, you will need to add an extra
            check to make sure you are not in any other plot. It is not clear how to
            go about this.
            Since we also want this to work in loglog plot, we work in axes
            coordinates and use the proper scaling transform to convert to data
            limits."""

            x, y = event.x, event.y
            tranP2A = ax.transAxes.inverted().transform  # display to axes
            tranA2D = ax.transLimits.inverted().transform  # ax to data
            tranSclA2D = ax.transScale.inverted().transform  # data to scale

            scale = [base_scale, 1 / base_scale][event.button == "up"]
            xa, ya = tranP2A((x, y))
            zoomx, zoomy = bool((xa > 0) & (xa < 1)), bool((ya > 0) & (ya < 1))
            scaledlim = 0.5 * np.array([1 - scale, 1 + scale])
            xlim, ylim = [(0, 1), scaledlim][zoomx], [(0, 1), scaledlim][zoomy]
            xd, yd = tranSclA2D(tranA2D(np.array([xlim, ylim]).T)).T  # data coords
            ax.set_xlim(xd)
            ax.set_ylim(yd)
            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest
        fig.canvas.mpl_connect("scroll_event", zoom)
        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            # rescale to full extent if key is pressed.
            if event.key is not None:  # doesn't currently work
                ax.relim()
                ax.autoscale_view(True, True, True)
                return

            if event.button == 3:
                if event.inaxes != ax:
                    return
                self.cur_xlim = ax.get_xlim()
                self.cur_ylim = ax.get_ylim()
                self.press = self.x0, self.y0, event.xdata, event.ydata
                self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            if event.button == 3:
                self.press = None
                ax.figure.canvas.draw()

        def onMotion(event):
            if event.button == 3:
                if self.press is None:
                    return
                if event.inaxes != ax:
                    return
                dx = event.xdata - self.xpress
                dy = event.ydata - self.ypress
                self.cur_xlim -= dx
                self.cur_ylim -= dy
                ax.set_xlim(self.cur_xlim)
                ax.set_ylim(self.cur_ylim)

                ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect("button_press_event", onPress)
        fig.canvas.mpl_connect("button_release_event", onRelease)
        fig.canvas.mpl_connect("motion_notify_event", onMotion)

        # return the function
        return onMotion
