"""
Submodule for reading the native `.lase` and `.scancsv` files from the Chromium software
from a Teledyne/Photonmachines laser ablation system.
"""

import re
import numpy as np
import pandas as pd
from pathlib import Path


def split_config(s):
    """
    Splits a config-formatted string.

    Parameters
    ----------
    s : :class:`str`

    Returns
    ---------
    :class:`dict`

    See Also
    ---------
    :func:`get_scandata`
    """
    x = re.split(r";", s)
    d = {k: v for (k, v) in [i.split("=") for i in x]}
    return d


def read_lasefile(filepath, encoding="cp1252"):
    """
    Read a .lase formatted file into a :class:`~pandas.DataFrame`.

    Parameters
    ----------
    filepath : :class:`str`, :class:`pathlib.Path`
        Path to the .lase file to import.
    encoding : :class:`str`
        File encoding of the .lase file.

    Returns
    ---------
    :class:`~pandas.DataFrame`

    Notes
    -------

    `.lase` files have all spot information as well as gas flows and all control options
    of laser operation. These are configuration files structured by blocks demarkated
    with square brackets, along the lines of::

        [Scans]
        Header=Scan Type,Description, ...
        Scan0=Spot,"Spot 1", ...
        [<other control blocks>]
        ...

    Some of the values in this table are string-encoded tuples
    (e.g. :code:`"57950.00,37530.00,20734.50"`) and dictionaries
    (e.g. :code:`"Dosage=1;DwellTime=1.00;LineSpacing=100.00;Laser.Output=10.00;..."`).

    See Also
    ---------
    :class:`ScanData`
    """
    path = Path(filepath)
    if not path.suffix == ".lase":
        path = path.with_suffix(".lase")
    file = open(str(path), encoding=encoding).read()
    lines = [i for i in re.split("[\n\r]", file) if i]

    data = {}
    for l in lines:
        if re.match(r"^\[.*\]$", l):
            section = l.replace("[", "").replace("]", "")
            data[section] = {}
        else:
            var, value = re.split("=", l, maxsplit=1)
            data[section][var] = value

    df = get_scandata(data["Scans"])
    return df


def read_scancsv(filename, encoding="cp1252"):
    """
    Read a .scancsv formatted file.

    Parameters
    ----------
    filepath : :class:`str`, :class:`pathlib.Path`
        Path to the .scancsv file to import.
    encoding : :class:`str`
        File encoding of the .scancsv file.

    Returns
    ---------
    :class:`pandas.DataFrame`

    Notes
    --------

    `.scancsv` files only contain spot information and do not edit the laser and gas
    conditions. These are essentially comma-separated values files, with a structure
    along the lines of::

        Scan Type,Description, ...
        Spot,"Spot 1", ...

    Some of the values in this table are string-encoded tuples
    (e.g. :code:`"57950.00,37530.00,20734.50"`) and dictionaries
    (e.g. :code:`"Dosage=1;DwellTime=1.00;LineSpacing=100.00;Laser.Output=10.00;..."`).

    See Also
    ---------
    :class:`ScanData`
    """
    path = Path(filename)
    if not path.suffix == ".scancsv":
        path = path.with_suffix(".scancsv")
    scanfile = open(str(path), encoding=encoding).read()  # .readlines()
    scanfilelines = [i for i in re.split("[\n\r]", scanfile) if i]

    scanfiledict = {}
    scanfiledict["Header"] = scanfilelines[0]
    for ix, l in enumerate(scanfilelines[1:]):
        scanfiledict[ix] = l

    df = get_scandata(scanfiledict)
    return df


def get_scandata(scandict):
    """
    Process a dictionary of scan information into a :class:`~pandas.DataFrame`.

    Parameters
    ----------
    scandict : :class:`dict`
        Dictionary of scan data.

    Returns
    ---------
    :class:`pandas.DataFrame`

    See Also
    ---------
    :class:`ScanData`
    """
    headers = scandict["Header"].split(",")
    scannames = [i for i in scandict.keys() if not i == "Header"]
    no_scans = len(scannames)
    df = pd.DataFrame(columns=headers, index=scannames)
    for s in scannames:
        scandata = re.findall(r'".+?"|[\w-]+', scandict[s])
        df.loc[s, headers[: len(scandata)]] = scandata

    for c in [
        "Description",
        "Vertex List",
        "Preablation Settings",
        "Ablation Settings",
    ]:
        df[c] = df[c].str.replace('"', "")

    df["Vertex List"] = (
        df["Vertex List"]
        .str.split(";")
        .apply(lambda x: np.array([i.split(",") for i in x]))
    )
    df["Preablation Settings"] = df["Preablation Settings"].apply(split_config)
    df["Ablation Settings"] = df["Ablation Settings"].apply(split_config)
    df["Data"] = df["Data"].apply(split_config)
    return df


class ScanData(object):
    def __init__(self, datapath):
        self.default_z = 20800
        self.load_data(datapath)

    def load_data(self, datapath):
        data = Path(datapath)
        if "lase" in data.suffix:
            self.df = read_lasefile(datapath)
        else:
            self.df = read_scancsv(datapath)

    def get_verticies(self):
        verts = (
            np.vstack(self.df["Vertex List"].map(np.array).values)
            .reshape(self.df.index.size, -1)
            .astype(np.float)
        )
        return pd.DataFrame(verts, index=self.df.Description, columns=["x", "y", "z"])

    def __repr__(self):
        return self.df.__repr__()
