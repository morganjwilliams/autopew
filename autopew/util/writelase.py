"""
Write a set of x-y coords to a .scancsv file.
"""
from pathlib import Path
import numpy as np
import pandas as pd


def xy2scansv(xy, filename="testfile", z=20800, spotname_prefix="Spot"):
    """
    Write x-y coordinates to a laser.scancsv file.

    Todo
    ------

        * Take spot numbers from imported point list index
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
    df[
        "Preablation Settings"
    ] = "'Dosage=1;DwellTime=1.00;LineSpacing=100.00;Laser.Output=10.00;LineScanMode=1;PassCount=1;Laser.RepRate=1.00;ScanSpeed=50.00;PassEnabled=0;ShotCount=1;SpotSpacing=100.00;Laser.SpotSize=150μm Circle;Laser.SpotRotation=0.00'"
    df[
        "Ablation Settings"
    ] = "'Dosage=0;DwellTime=1.00;LineSpacing=0.00;Laser.Output=60.10;LineScanMode=1;PassCount=1;Laser.RepRate=9.00;ScanSpeed=0.00;PassEnabled=1;ShotCount=260;SpotSpacing=0.00;Laser.SpotSize=50μm Circle;Laser.SpotRotation=0.00'"
    df["Data"] = "'ExpectedLaseTime=28.9;ScanLength=0.0'"
    with open(Path(filename).with_suffix(".scancsv"), "wb") as f:
        str = df.to_csv(index=False).encode("utf-8")
        f.write(str)
    return df


df = xy2scansv(np.array([[1.0, 2.0], [1.1, 2.1]]))
