import matplotlib.pyplot as plt


def close_event():
    plt.close()  # timer calls this function after 3 seconds and closes the window


def add_timeout(fig, timeout=10000):
    timer = fig.canvas.new_timer(interval=timeout)
    timer.add_callback(close_event)

    def reset_timer():
        timer.stop()
        timer = None
        timer = fig.canvas.new_timer(interval=timeout)
        timer.add_callback(close_event)
        fig.timer = timer

    fig.timer = timer
    fig.timer.reset = reset_timer
