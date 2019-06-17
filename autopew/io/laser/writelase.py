"""
Write a set of x-y coords to a .scancsv file.
"""
from pathlib import Path
import numpy as np
import pandas as pd


def xy2scansv(xy, filename="testfile", z=20800, spotname_prefix="Spot"):
    """
    Write x-y coordinates to a laser.scancsv file.

    Returns
    --------
    :class:`pandas.DataFrame`

    Todo
    ------

        * Take spot numbers/names from imported point list index
        * Take spot sizes from imported point list
        * Output encoding to match input scansv (it's not UTF-8, issues with spotsize)
    """
    x, y = xy.T

    df = pd.DataFrame(
        columns="Scan Type,Description,Selected,Lock Edit,Vertex Count,Vertex List,Preablation Settings,Ablation Settings,Data".split(
            ","
        ),
        index=range(xy.shape[0]),
    )

    df["Scan Type"] = "Spot"
    df.Description = ["{} {:d}".format(spotname_prefix, ix + 1) for ix in range(len(x))]
    df.Selected = 1
    df["Lock Edit"] = 0
    df["Vertex Count"] = 1
    df["Vertex List"] = ["{:.2f},{:.2f},{:.2f}".format(*row, z) for row in xy]
    preablate, ablate, data = (
        u"'Dosage=1;DwellTime=1.00;LineSpacing=100.00;Laser.Output=10.00;LineScanMode=1;PassCount=1;Laser.RepRate=1.00;ScanSpeed=50.00;PassEnabled=0;ShotCount=1;SpotSpacing=100.00;Laser.SpotSize=150\xb5m Circle;Laser.SpotRotation=0.00'",
        u"'Dosage=0;DwellTime=1.00;LineSpacing=0.00;Laser.Output=60.10;LineScanMode=1;PassCount=1;Laser.RepRate=9.00;ScanSpeed=0.00;PassEnabled=1;ShotCount=260;SpotSpacing=0.00;Laser.SpotSize=50\xb5m Circle;Laser.SpotRotation=0.00'",
        "",
    )
    df["Data"] = data
    df["Preablation Settings"] = preablate
    df["Ablation Settings"] = ablate
    return df
