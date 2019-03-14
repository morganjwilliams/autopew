import matplotlib.pyplot as plt
import numpy as np
import logging
from matplotlib.backends.backend_qt5 import TimerBase

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def timer_reset(self, *args, **kwargs):
    """
    Timer reset for TimerQT objects.
    """
    self._timer.stop()
    self._timer.setInterval(self._interval)
    logger.info('Timer Reset: ')
    self._timer.start()

setattr(TimerBase, "reset", timer_reset)


def _timeout(fig, timeout=1000):
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

            x = event.x
            y = event.y

            # convert pixels to axes
            tranP2A = ax.transAxes.inverted().transform
            # convert axes to data limits
            tranA2D = ax.transLimits.inverted().transform
            # convert the scale (for log plots)
            tranSclA2D = ax.transScale.inverted().transform

            if event.button == "down":
                # deal with zoom in
                scale_factor = base_scale
            elif event.button == "up":
                # deal with zoom out
                scale_factor = 1 / base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1

            # get my axes position to know where I am with respect to them
            xa, ya = tranP2A((x, y))
            zoomx = False
            zoomy = False
            if ya < 0:
                if xa >= 0 and xa <= 1:
                    zoomx = True
                    zoomy = False
            elif ya <= 1:
                if xa < 0:
                    zoomx = False
                    zoomy = True
                elif xa <= 1:
                    zoomx = True
                    zoomy = True
                else:
                    zoomx = False
                    zoomy = True
            else:
                if xa >= 0 and xa <= 1:
                    zoomx = True
                    zoomy = False

            new_alimx = (0, 1)
            new_alimy = (0, 1)
            if zoomx:
                new_alimx = (np.array([1, 1]) + np.array([-1, 1]) * scale_factor) * 0.5
            if zoomy:
                new_alimy = (np.array([1, 1]) + np.array([-1, 1]) * scale_factor) * 0.5

            # now convert axes to data
            new_xlim0, new_ylim0 = tranSclA2D(tranA2D((new_alimx[0], new_alimy[0])))
            new_xlim1, new_ylim1 = tranSclA2D(tranA2D((new_alimx[1], new_alimy[1])))

            # and set limits
            ax.set_xlim([new_xlim0, new_xlim1])
            ax.set_ylim([new_ylim0, new_ylim1])
            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest
        fig.canvas.mpl_connect("scroll_event", zoom)
        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax:
                return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
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
