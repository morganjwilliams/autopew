import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

class Point(object):
    def __init__(coords, *args, **kwargs):
        self.coords = coords


class Line(object):
    def __init__(coords, *args, **kwargs):
        self.coords = coords


class Map(object):
    def __init__(coords, *args, **kwargs):
        self.coords = coords
