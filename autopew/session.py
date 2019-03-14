import json
import logging
from .targets import Point, Line, Map

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

class Session(object):
    """
    Session objects to store context for analytical sessions.
    """

    def __init__(self, report_template=None):

        self.report_template = report_template

    def add_point(self, point):
        pass

    def add_line(self, line):
        pass

    def add_map(self, map):
        pass

    def to_scancsv(self):
        """Create a .scancsv file."""
        pass

    def dump(self):
        """Dump configuration to json"""
        pass

    def report(self, template=None):
        pass
