# Note: this needs to be executed from a terminal for gui functionality

from autopew.session import Session
from pathlib import Path
import numpy as np
from autopew.util.meta import autopew_datafolder
from autopew.io.laser.writelase import xy2scansv

from pyrolite.util.meta import stream_log

stream_log("autopew.session")

img = "NOR1-3B", autopew_datafolder("images") / "NOR1-3B.jpg"  # image
newpoints = autopew_datafolder() / "NOR1-3B.csv"  #
scancsv = autopew_datafolder("examples") / "autopew_test.scancsv"  # coordination points
# pixel coordinates of reference points R1-R3
pc = np.array([[2603.5, 5224.7], [613.59, 1173.97], [2357.6, 441.7]])

s = Session()
newverts = s.autoflow(
    img=img,
    dest_coord=scancsv.resolve(),
    src_coord=None,
    src_points=newpoints.resolve(),
)

df = xy2scansv(newverts, spotname_prefix="NOR1-3B")


encoding = "cp1252"
with open(Path("testfile").with_suffix(".scancsv"), "w", encoding=encoding) as f:
    str = df.to_csv(index=False, encoding=encoding)
    f.write(str)
