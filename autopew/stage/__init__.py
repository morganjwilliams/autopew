import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


class Stage(object):
    def __int__(self, limits=None):
        self.limits = limits

    def get_limits(self):
        return self.limits


# create stage <--> image transforms (2D), stage <--> stage transforms (3D)
