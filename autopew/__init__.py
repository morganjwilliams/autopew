import sys
import logging
import pathlib
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.captureWarnings(True)

from . import transform, image, gui, graph, io, workflow

__all__ = ["transform", "image", "gui", "graph", "io", "workflow"]

from autopew.io import get_filehandler


class Pew(object):
    def __init__(self, *args, **kwargs):
        self._transform = None
        self.transformed = None

        if len(args) == 2:  # calibrate using src-dest
            self.calibrate(*args)
        elif len(args) == 1:  # pre-defined transform?
            # check that object is a transform or transform matrix
            self._transform = args[0]
        else:
            raise NotImplementedError("Unrecognised initialization arguments supplied.")

    def _read(self, filepath, handler=None, **kwargs):

        if isinstance(filepath, (np.ndarray, pd.DataFrame, list)):
            return pd.DataFrame(filepath)
        elif isinstance(filepath, (str, pathlib.Path)):
            handler = get_filehandler(filepath, name=handler, **kwargs)
        return handler.read(filepath)

    def _write(self, obj, filepath, handler=None, **kwargs):

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
