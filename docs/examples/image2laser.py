# Note: this needs to be executed from a terminal for gui functionality

from autopew.session import Session
from pathlib import Path
from autopew.util.meta import autopew_datafolder
from autopew.io.laser.writelase import xy2scansv

s = Session()
img = "NOR1-3B", autopew_datafolder("images") / "NOR1-3B.jpg"  # image
newpoints = autopew_datafolder() / "NOR1-3B.csv"  #
scancsv = autopew_datafolder("examples") / "autopew_test.scancsv"  # coordination points

newverts = s.autoflow(img, scancsv.resolve(), newpoints.resolve())

df = xy2scansv(newverts, spotname_prefix="NOR1-3B")

encoding = "cp1252"
with open(Path("testfile").with_suffix(".scancsv"), "w", encoding=encoding) as f:
    str = df.to_csv(index=False, encoding=encoding)
    f.write(str)
