import re
import numpy as np
import pandas as pd
from pathlib import Path


def split_config(s):
    """
    Splits a config-formatted string.

    Returns
    ---------
    :class:`str`
    """
    x = re.split(r";", s)
    d = {k: v for (k, v) in [i.split("=") for i in x]}
    return d


def read_lasefile(filename, encoding="cp1252"):
    """
    Read a .lase formatted file.

    Returns
    ---------
    :class:`dict`

    Todo
    ------

        * DataFrame return
    """
    path = Path(filename)
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

    return data


def get_scandata(scandict):
    """
    Process a dictionary of scan information into a Pandas DataFrame.

    Returns
    ---------
    :class:`pandas.DataFrame`
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


def read_scancsv(filename, encoding="cp1252"):
    """
    Read a .scancsv formatted file.

    Returns
    ---------
    :class:`pandas.DataFrame`
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

    data = get_scandata(scanfiledict)
    return data


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
