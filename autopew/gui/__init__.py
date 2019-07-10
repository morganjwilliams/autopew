import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

from . import base
from . import windows

__all__ = ['base', 'windows']
