import re
import numpy as np
import pandas as pd
from pathlib import Path


def read_lasefile(filename):
    """
    Read a .lase formatted file.
    """
    path = Path(filename)
    if not path.suffix == ".lase":
        path = path.with_suffix(".lase")
    file = open(path, encoding="cp1252").read()
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


def read_scancsv(filename):
    """
    Read a .scancsv formatted file.
    """
    path = Path(filename)
    if not path.suffix == ".scancsv":
        path = path.with_suffix(".scancsv")
    scanfile = open(path, encoding="cp1252").read()  # .readlines()
    scanfilelines = [i for i in re.split("[\n\r]", scanfile) if i]

    scanfiledict = {}
    scanfiledict["Header"] = scanfilelines[0]
    for ix, l in enumerate(scanfilelines[1:]):
        scanfiledict[ix] = l

    data = get_scandata(scanfiledict)
    return data


def split_config(s):
    """
    Splits a config-formatted string.
    """
    x = re.split(r";", s)
    d = {k: v for (k, v) in [i.split("=") for i in x]}
    return d


def get_scandata(scandict):
    headers = scandict["Header"].split(",")
    scannames = [i for i in scandict.keys() if not i == "Header"]
    no_scans = len(scannames)
    df = pd.DataFrame(columns=headers, index=scannames)
    for s in scannames:
        scandata = re.findall(r'".+?"|[\w-]+', scandict[s])
        df.loc[s, headers] = scandata

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
    def __init__(self, data):

        self.default_z = 20800
        self.load_data(data)

    def load_data(self, data):
        if isinstance(data, dict):
            self.df = get_scandata(dict)
        elif isinstance(data, str) or isinstance(data, Path):
            data = Path(data)
            if "lase" in data.suffix:
                self.df = read_lasefile(data)
            else:
                self.df = read_scancsv(data)

    def get_verticies(self):
        verts = np.vstack(self.df["Vertex List"].map(np.array).values).reshape(
            self.df.index.size, -1
        ).astype(np.float)
        return pd.DataFrame(verts, index=self.df.Description, columns=["x", "y", "z"])

    def __repr__(self):
        return self.df.__repr__()
