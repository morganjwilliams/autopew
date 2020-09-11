import sys
import json
import logging
import pathlib
import pandas as pd
import numpy as np
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.captureWarnings(True)

from . import transform, image, gui, graph, io, workflow

__all__ = ["transform", "image", "gui", "graph", "io", "workflow"]

from autopew.io import get_filehandler

# pandas dataframe accessor for verifying dataframe structure and accessing coordinates?


class Pew(object):
    def __init__(self, *args, transform=None, archive=None, **kwargs):
        self._transform = transform
        self.transformed = None

        if archive is not None:
            self._load_from_archive(archive)
        else:
            if args:
                if len(args) == 2:  # calibrate using src-dest
                    self.calibrate(*args)
                else:
                    raise NotImplementedError(
                        "Unrecognised initialization arguments supplied."
                    )

    def _read(self, filepath, handler=None, **kwargs):
        filepath = pathlib.Path(filepath)
        if isinstance(filepath, (np.ndarray, pd.DataFrame, list)):
            return pd.DataFrame(filepath)
        elif isinstance(filepath, (str, pathlib.Path)):
            handler = get_filehandler(filepath, name=handler, **kwargs)
        return handler.read(filepath)

    def _write(self, obj, filepath, handler=None, **kwargs):
        filepath = pathlib.Path(filepath)
        if isinstance(filepath, (str, pathlib.Path)):
            handler = get_filehandler(filepath, name=handler, **kwargs)
        else:
            raise NotImplementedError("Invalid export filepath.")
        return handler.write(obj)

    def calibrate(self, src, dest, handler=None):
        """
        Calibrate the transformation between two planar coordinate systems given
        two sets of corresponding points.

        Parameters
        -------------
        src : :class:`str` | :class:`pathlib.Path` | :class:`numpy.ndarray` | :class:`pandas.DataFrame`
        dest: :class:`str` | :class:`pathlib.Path` | :class:`numpy.ndarray` | :class:`pandas.DataFrame`
        handler : :class:`str` | :class:`tuple`

        """
        # deal with potential for two handler names to be passed
        if handler is not None:
            if isinstance(handler, str):
                handlers = [handler, handler]
            else:
                if not len(handlers) == 2:
                    raise IndexError("Invalid handler argument.")
                handlers = handler
        else:
            handlers = [None, None]

        self.src, self.dest = (
            self._read(src, handler=handlers[0]),
            self._read(handler=handlers[0]),
        )
        self._transform = affine_transform(affine_from_AB(self.src, self.dest))

    def load(self, filepath, handler=None):
        """
        Import a set of sample coordinates.

        Parameters
        -------------
        filepath : :class:`str` | :class:`pathlib.Path` | :class:`numpy.ndarray` | :class:`pandas.DataFrame`

        Returns
        -------
        :class:`pandas.DataFrame`
        """
        self.samples = self._read(filepath, handler=handler)
        return self.samples  # return imported coordinates?

    def transform(self, limits=None):
        """
        Transform source coordinates to the destination coordinate system.

        Parameters
        ----------
        limits : :class:`list` | :class:`numpy.ndarray`

        Returns
        -------
        :class:`numpy.ndarray`
        """
        if self._transform is None:
            raise NotCalibratedError("Transform hasn't yet been calibrated.")
        self.transformed = self._transform(self.samples)  # apply to dataframe or array?
        return (
            self.transformed
        )  # return values so that quick queries can be made without exporting

    def export(self, filepath):
        """
        Export a set of coordinates.

        Parameters
        -------------
        filepath: :class:`str` | :class:`pathlib.Path`
        """
        # make sure the sample inputs have been transformed
        if self.transformed is None:
            self.transform()
        self._write(self.transformed, filepath)

    def archive(self, filepath):
        """
        Archive the coordinate mapping and calibration for later loading.

        Parameters
        ----------
        filepath: :class:`str` | :class:`pathlib.Path`
        """
        fp = pathlib.Path(filepath)
        if fp.suffix not in [".pew", ".json"]:
            msg = (
                "Archive filepath has an invalid extension; "
                "please use either '.pew' or '.json'."
            )
            raise AssertionError(msg)

        data = {}
        # get calibration coordinates

        # get sample points

        # get affine transform array

        # store info as JSON
        json.dump(data, fp)

    def _load_from_archive(self, filepath):
        """
        Load the Pew map from an archived file.

        Parameters
        ----------
        filepath: :class:`str` | :class:`pathlib.Path`
        """
        fp = pathlib.Path(filepath)
        if fp.suffix not in [".pew", ".json"]:
            msg = (
                "Archive filepath has an invalid extension; "
                "please use either '.pew' or '.json'."
            )
            raise AssertionError(msg)
        # load from JSON
        with open(fp, "r") as f:
            data = json.loads(f.read())
        # add calibration coordinates

        # get affine transform array

        # verify integrity between calibration and transform array

        # get sample points
