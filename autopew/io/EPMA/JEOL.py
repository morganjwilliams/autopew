"""
Export function for the JEOL field-emission gun electron probe microanalyser (EPMA)
using "probe for EPMA".
"""
import csv
import numpy as np
import pandas as pd
from pathlib import Path


def write_pos(
    df, filepath=Path("./exportedpoints.pos"), encoding="cp1252", z=10.7, **kwargs
):
    """
    Export an dataframe of coordinates to a .pos file.

    Parameters
    ------------
    df : :class:`pandas.DataFrame`
        Dataframe containing points to serialise.
    filepath : :class:`str` | :class:`pathlib.Path`
        Filepath for export.
    encoding : :class:`str`
        Encoding for the output file.
    z : :class:`int`
        Optional specification of default focus value to use.

    Returns
    --------
    :class:`pandas.DataFrame`

    """

    # requires FOCUS, X, Y, spotnames
    # lets save them so we can directly import them
    pos = pd.DataFrame(
        index=df.index,
        columns=[
            "two",
            "index",
            "label",
            "X",
            "Y",
            "Z",
            "type1",
            "type2",
            "type3",
            "type4",
            "blank",
        ],
    )
    pos["two"] = 2
    pos["index"] = df.index + 1
    pos["label"] = df["name"].apply(lambda x: '"' + str(x) + '"')
    pos["X"] = df["x"]
    pos["Y"] = df["y"]
    pos["Z"] = z
    pos["type1"] = 0
    pos["type2"] = 1
    pos["type3"] = 0
    pos["type4"] = 0
    pos["blank"] = '""'

    # export to text file with no blank row at end
    s = pos.to_csv(None, quoting=csv.QUOTE_NONE, index=False, header=False)
    s = s.replace("\r\n", "\n")
    s = "0,0,0,0\n0,0,0,0\n0,0,0,0\n" + s
    with open(str(filepath), "w") as f: # str for Python 3.5 compatibility
        f.write(s[:-1])
