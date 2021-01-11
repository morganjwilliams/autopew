import sys, inspect
from pathlib import Path
import pandas as pd
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

from . import laser
from . import EPMA

__all__ = ["laser"]


class PewIOSpecification(object):
    """
    Template for input and output file handlers for autopew.

    These handers specify functions to import files to pandas DataFrames and the
    export of these filetypes from pandas DataFrames.
    """

    extension = None
    type = None  # type handlers for np.array, pd.DataFrame?

    # could add _read, _write, _verify methods which are then customized?
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def validate_dataframe(cls, df):
        """
        Validate the output of a file reader against the minimum requirements
        for autopew.

        Parameters
        ----------
        df : :class:`pandas.DataFrame`
            Dataframe to validate.
        """
        try:  # check input type
            assert isinstance(df, pd.DataFrame)
        except AssertionError as e:
            msg = "File reader needs to provide a pandas DataFrame."
            logger.warning(msg)
            raise e

        # check columns
        required = ["name", "x", "y"]
        absent = [c for c in required if c not in df.columns]
        if absent:
            msg = "Input dataframe missing required column(s): {}.".format(
                ", ".join(absent)
            )
            logger.warning(msg)
            raise AssertionError(msg)


class PewCSV(PewIOSpecification):
    extension = ".csv"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def read(self, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        self.validate_dataframe(df)
        return df

    @classmethod
    def write(self, df, filepath, **kwargs):
        self.validate_dataframe(df)
        return df.to_csv(
            str(filepath.with_suffix(self.extension)), **kwargs
        )  # str for  # compatibility for Python 3.5


class PewSCANCSV(PewIOSpecification):
    extension = ".scancsv"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def read(self, filepath):
        df = laser.chromium.read_scancsv(filepath)
        self.validate_dataframe(df)
        return df

    @classmethod
    def write(self, df, filepath, **kwargs):
        self.validate_dataframe(df)
        return laser.chromium.write_scancsv(
            df, filepath.with_suffix(self.extension), **kwargs
        )


class PewJEOLpos(PewIOSpecification):
    extension = ".pos"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def write(self, df, filepath, **kwargs):
        self.validate_dataframe(df)
        return EPMA.JEOL.write_pos(df, filepath.with_suffix(self.extension), **kwargs)


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


def get_filehandler(filepath=None, name=None):
    """
    Get a registered file handler for autopew.

    Parameters
    ----------
    filepath : :class:`str` | :class:`pathlib.Path`
        Filename or path to the file you want to read/write.
    name : :class:`str`
        Name of the file handler to use (subclass of :class:`PewIOSpecification`).

    Returns
    -------
    handler : :class:`PewIOSpecification`
    """
    if filepath is None and name is None:
        msg = "Please specify either a filename, handler name or both."
        raise NotImplementedError(msg)

    exts = registered_extensions()
    if name is None:
        # lookup by file only

        # get file extension
        ext = Path(filepath).suffix
        if ext in [None, ""]:
            raise NotImplementedError(
                "No extension found for file {}.".format(filepath)
            )

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
