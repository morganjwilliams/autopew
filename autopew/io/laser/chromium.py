"""
Import and export functions for the Chromium Laser Ablation Navigation Software.
"""
import re
import csv
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

    Todo
    -----
    Consider using :mod:`configparser` to read .lase files.
    """
    x = re.split(r";", s)
    d = {k: v for (k, v) in [i.split("=") for i in x]}
    return d


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


def read_lasefile(filepath, encoding="cp1252"):
    """
    Read a .lase formatted file into a dictonary (one item per scan), and
    return this in the form of a :class:`~pandas.DataFrame`.

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
    (e.g. `"57950.00,37530.00,20734.50"`) and dictionaries
    (e.g. `"Dosage=1;DwellTime=1.00;LineSpacing=100.00;Laser.Output=10.00;..."`).

    See Also
    ---------
    :class:`ScanData`
    :func:`get_scandata`
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


def read_scancsv(filepath, encoding="cp1252"):
    """
    Read a .scancsv into a dictonary (one item per scan), and
    return this in the form of a :class:`~pandas.DataFrame`.

    Parameters
    ----------
    filepath : :class:`str`, :class:`pathlib.Path`
        Path to the .scancsv file to import.
    encoding : :class:`str`
        File encoding of the .scancsv file.

    Returns
    ---------
    :class:`~pandas.DataFrame`

    Notes
    --------

    `.scancsv` files only contain spot information and do not edit the laser and gas
    conditions. These are essentially comma-separated values files, with a structure
    along the lines of::

        Scan Type,Description, ...
        Spot,"Spot 1", ...

    Some of the values in this table are string-encoded tuples
    (e.g. `"57950.00,37530.00,20734.50"`) and dictionaries
    (e.g. `"Dosage=1;DwellTime=1.00;LineSpacing=100.00;Laser.Output=10.00;..."`).

    See Also
    ---------
    :class:`ScanData`
    :func:`get_scandata`
    """
    path = Path(filepath)
    if not path.suffix == ".scancsv":
        path = path.with_suffix(".scancsv")
    scanfile = open(str(path), encoding=encoding).read()  # .readlines()
    scanfilelines = [i for i in re.split("[\n\r]", scanfile) if i]

    scanfiledict = {}
    scanfiledict["Header"] = scanfilelines[0]
    for ix, l in enumerate(scanfilelines[1:]):
        scanfiledict[ix] = l

    df = get_scandata(scanfiledict)
    df = df.reindex(columns=["name", "x", "y", "z"] + df.columns.tolist())
    df[["x", "y", "z"]] = (
        np.vstack(df["Vertex List"].map(np.array).values)
        .reshape(df.index.size, -1)
        .astype(np.float)
    )
    # pd.DataFrame(verts, index=df.Description, columns=["x", "y", "z"])
    return df


def write_scancsv(
    df,
    filepath=Path("./exportedpoints.scancsv"),
    spotnames=None,
    encoding="cp1252",
    z=20800,
    **kwargs
):
    """
    Export an array of coordinates to a .scancsv file.

    Parameters
    ------------
    df : :class:`pandas.DataFrame`
        Dataframe containing points to serialise.
    filepath : :class:`str` | :class:`pathlib.Path`
        Filepath for export.
    spotnames : :class:`str` | :class:`list`
        Name to prefix spot indicies or a list of spot names.
    encoding : :class:`str`
        Encoding for the output file.
    z : :class:`int`
        Optional specification of default focus value to use.

    Returns
    --------
    :class:`pandas.DataFrame`

    Todo
    ------
        * Take spot numbers/names from imported point list index
        * Take spot sizes from imported point list
        * Output encoding to match input scansv (it's not UTF-8, issues with spotsize)
    """
    scancsv = pd.DataFrame(
        columns=(
            "Scan Type,Description,Selected,Lock Edit,Vertex Count,"
            "Vertex List,Preablation Settings,Ablation Settings,Data"
        ).split(","),
        index=range(df.index.size),
    )

    scancsv["Scan Type"] = "Spot"
    if spotnames is not None:
        if isinstance(spotnames, str):
            scancsv["Description"] = [
                "{}_{:d}".format(spotnames, ix + 1) for ix in range(df.index.size)
            ]
        else:
            assert len(spotnames) == scancsv.index.size
            scancsv["Description"] = list(spotnames)
    else:
        scancsv["Description"] = ["{:d}".format(ix + 1) for ix in range(df.index.size)]
    scancsv.Selected = 1
    scancsv["Lock Edit"] = 0
    scancsv["Vertex Count"] = 1
    scancsv["Vertex List"] = [
        "{:.2f},{:.2f},{:.2f}".format(*df.loc[ix, ["x", "y"]].values, z)
        for ix in df.index
    ]
    preablate, ablate = (
        "Dosage=1;DwellTime=1.00;LineSpacing=100.00;Laser.Output=10.00;LineScanMode=1;PassCount=1;Laser.RepRate=1.00;ScanSpeed=50.00;PassEnabled=0;ShotCount=1;SpotSpacing=100.00;Laser.SpotSize=150\xb5m Circle;Laser.SpotRotation=0.00",
        "Dosage=0;DwellTime=1.00;LineSpacing=0.00;Laser.Output=60.10;LineScanMode=1;PassCount=1;Laser.RepRate=9.00;ScanSpeed=0.00;PassEnabled=1;ShotCount=260;SpotSpacing=0.00;Laser.SpotSize=50\xb5m Circle;Laser.SpotRotation=0.00",
    )
    scancsv["Data"] = "ExpectedLaseTime=28.9;ScanLength=0.0"
    scancsv["Preablation Settings"] = preablate
    scancsv["Ablation Settings"] = ablate
    output_filepath = Path(filepath).with_suffix(".scancsv")
    with open(
        str(output_filepath), "w", encoding=encoding
    ) as f:  # str for Python 3.5 compatibility
        f.write(",".join(scancsv.columns.tolist()) + "\n")
        buffer = scancsv.to_csv(
            header=False, index=False, encoding=encoding, quoting=csv.QUOTE_NONNUMERIC
        )
        f.write(buffer)
    return scancsv
