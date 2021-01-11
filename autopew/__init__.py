"""
Base module for autopew containing the core object oriented API.

Todo
----
* Implement pandas dataframe accessor for quick export of dataframes to specific
    filetypes (e.g. `df.pew.to_scancsv()`; with dataframe validators).
"""
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

from .io import get_filehandler, PewIOSpecification
from .transform.affine import affine_transform, affine_from_AB

# pandas dataframe accessor for verifying dataframe structure and accessing coordinates?


class Pew(object):
    def __init__(self, *args, transform=None, archive=None, **kwargs):
        """
        Pew transformer which implements various file handlers for import and export of
        sample coordinates.
        """
        self._transform = transform
        self.transformed = None
        self.samples = None

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

    def _read(self, src, handler=None, **kwargs):
        if isinstance(src, (np.ndarray, pd.DataFrame, list)):
            shape = np.array(src).shape
            if shape[1] == 2:  # (n, 2) array without names
                df = pd.DataFrame(src)
                df.columns = ["x", "y"]
                df["name"] = np.arange(df.index.size)
                df["name"] = df["name"].astype("str")
                df = df.loc[:, ["name", "x", "y"]]
                return df
            elif shape[1] == 3:  # (n, 3) array with names
                df = pd.DataFrame(src)
                try:
                    PewIOSpecification.validate_dataframe(df)
                except:
                    df.columns = ["name", "x", y]
                return df
            else:
                msg = "Unknown form for datasource with shape: {}.".format(
                    ",".join(shape)
                )
                msg += " Source should have columns (x,y) or (name,x,y)."
                return NotImplementedError
        elif isinstance(src, (str, pathlib.Path)):
            filepath = pathlib.Path(src)
            if not isinstance(handler, PewIOSpecification):
                handler = get_filehandler(filepath, name=handler, **kwargs)
            return handler.read(filepath)
        else:
            raise NotImplementedError()

    def _write(self, obj, filepath, handler=None, **kwargs):
        filepath = pathlib.Path(filepath)
        if isinstance(filepath, (str, pathlib.Path)):
            handler = get_filehandler(filepath, name=handler)
        else:
            raise NotImplementedError("Invalid export filepath.")
        return handler.write(obj, filepath, **kwargs)

    def calibrate(self, src, dest, handler=None, **kwargs):
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
            self._read(src, handler=handlers[0], **kwargs),
            self._read(dest, handler=handlers[1], **kwargs),
        )
        self._transform = affine_transform(
            affine_from_AB(
                self.src[["x", "y"]].astype(float).values,
                self.dest[["x", "y"]].astype(float).values,
            )
        )
        if self.samples is not None:  # automatically transform loaded samples
            self.transform_samples()
        return self

    def load_samples(self, filepath, handler=None, **kwargs):
        """
        Import a set of sample coordinates.

        Parameters
        -------------
        filepath : :class:`str` | :class:`pathlib.Path` | :class:`numpy.ndarray` | :class:`pandas.DataFrame`

        Returns
        -------
        :class:`pandas.DataFrame`
        """
        self.samples = self._read(filepath, handler=handler, **kwargs)
        if self._transform is not None:  # automatically transform loaded samples
            self.transform_samples(**kwargs)
        return self

    def transform_samples(self, samples=None, limits=None, **kwargs):
        """
        Transform sample coordinates to the destination coordinate system.

        Parameters
        ----------
        limits : :class:`list` | :class:`numpy.ndarray`

        Returns
        -------
        :class:`numpy.ndarray`
        """
        if self._transform is None:
            raise NotCalibratedError("Transform hasn't yet been calibrated.")
        if samples is None:
            samples = self.samples
        if samples is None:
            raise IndexError("No samples have been loaded or provided.")
        self.transformed = self.samples.copy()
        # apply to dataframe or array?
        self.transformed[["x", "y"]] = self._transform(samples[["x", "y"]])
        # return values so that quick queries can be made without exporting
        return self

    def export_samples(self, filepath, enforce_transform=True, **kwargs):
        """
        Export a set of coordinates.

        Parameters
        -------------
        filepath: :class:`str` | :class:`pathlib.Path`
            Desired export filepath.
        enforce_transform : :class:`bool`
            Whether to enforce transformation before export.
        """
        # make sure the sample inputs have been transformed
        if enforce_transform and (self.transformed is None):
            self.transform_samples()
            self._write(self.transformed, filepath, **kwargs)
        else:
            self._write(self.samples, filepath, **kwargs)
        return self

    def to_archive(self, filepath):
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
        return self

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
