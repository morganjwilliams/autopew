import sys, inspect
from pathlib import Path
import pandas as pd
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

from . import laser

__all__ = ["laser"]


class PewIOSpecification(object):
    extension = None

    def __init__(self, *args, **kwargs):
        pass



def registered_extensions():
    """
    Get a dictionary of registered extensions mapping the relevant IO specifications.
    """
    specs = inspect.getmembers(
        sys.modules[__name__],
        lambda cls: issubclass(cls, PewIOSpecification)
        if inspect.isclass(cls)
        else False,
    )
    return {  # needs to be this way around to have duplicate extensions
        cls: cls.extension
        for (name, cls) in specs
        if cls.extension is not None  # ignore PewIOSpecification with extension=None
    }


def get_filehandler(file=None, name=None):
    """
    Get a registered file handler for autopew.

    Parameters
    ----------
    file : :class:`str` | :class:`pathlib.Path`
        Filename or path to the file you want to read/write.
    name : :class:`str`
        Name of the file handler to use (subclass of :class:`PewIOSpecification`).

    Returns
    -------
    handler : :class:`PewIOSpecification`
    """
    if file is None and name is None:
        msg = "Please specify either a filename, handler name or both."
        raise NotImplementedError(msg)

    exts = registered_extensions()
    if name is None:
        # lookup by file only

        # get file extension
        ext = Path(file).suffix
        if ext in [None, '']:
            raise NotImplementedError('No extension found for file {}.'.format(file))

        count = list(exts.values()).count(ext.lower())
        if not count:
            msg = (
                "Unrecognised file extension {}."
                "Check the docs for valid handlers.".format(name)
            )
            raise IndexError(msg)
        elif count > 1:
            msg = (
                "Multiple handlers found for extension {} -"
                "You'll need to specify the handler name."
            )
            raise IndexError(msg)
        else:
            handler = [k for k, v in exts.items() if v == ext.lower()][0]
            logger.debug("Handler found for {}: {}".format(ext, handler))
            return handler

    # lookup by name
    handlers = [cls for cls in exts.keys() if cls.__name__ == name]
    if not handlers:
        msg = (
            "PewIOSpec {} not found in registered handlers."
            "Check the docs for valid handlers.".format(name)
        )
        raise IndexError(msg)
    else:
        return handlers[0]
