import sys, inspect
from pathlib import Path
import pandas as pd
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

from . import laser
from ..workflow.laser import points_to_scancsv

__all__ = ["laser"]


class PewIOSpecification(object):
    extension = None
    type = None  # type handlers for np.array, pd.DataFrame?

    # could add _read, _write, _verify methods which are then customized?
    def __init__(self, *args, **kwargs):
        pass


class PewCSV(PewIOSpecification):
    extension = ".csv"

    def read(self, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        return df

    def write(self, df, filepath, **kwargs):
        return df.to_csv(filepath.with_suffix(self.extension), **kwargs)


class PewSCANCSV(PewIOSpecification):
    extension = ".scancsv"

    def read(self, filepath):
        df = laser.read_scancsv(filepath)
        return df

    def write(self, df, filepath, **kwargs):
        return points_to_scancsv(
            df[["x", "y"]], filepath.with_suffix(self.extension), **kwargs
        )


def registered_extensions():
    """
    Get a dictionary of registered extensions mapping the relevant IO specifications.

    Returns
    -------
    :class:`dict`
    """
    specs = inspect.getmembers(
        sys.modules[__name__],
        lambda cls: issubclass(cls, PewIOSpecification)
        if inspect.isclass(cls)
        else False,
    )
    return {  # needs to be this way around to allow duplicate extensions in values
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
        if ext in [None, ""]:
            raise NotImplementedError("No extension found for file {}.".format(file))

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
