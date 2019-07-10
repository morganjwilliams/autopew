import csv
import pandas as pd
from pathlib import Path
from ..io.laser.writelase import xy2scansv
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def points_to_scancsv(
    points,
    filename=Path("./exportedpoints.scancsv"),
    spotname_prefix="",
    encoding="cp1252",
    **kwargs
):
    """
    Export an array of coordinates to a .scancsv file.

    Parameters
    ------------
    points : :class:`numpy.ndarray`
        Points to serialise.
    filename : :class:`str` | :class:`pathlib.Path`
        Filename for export.
    spotname_prefix : :class:`str`
        Name to prefix spot indicies.
    encoding : :class:`str`
        Encoding for the output file.
    z : :class:`int`
        Optional specification of default focus value to use.
    """
    df = xy2scansv(points, spotname_prefix=spotname_prefix, **kwargs)
    with open(Path(filename).with_suffix(".scancsv"), "w", encoding=encoding) as f:
        f.write(",".join(df.columns.tolist()) + "\n")
        str = df.to_csv(
            header=False, index=False, encoding=encoding, quoting=csv.QUOTE_NONNUMERIC
        )
        f.write(str)
