"""
Submoudle for working with image data, used in interactive elements of autopew.
"""
import logging

from .base import PewImage

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

__all__ = ["PewImage"]
