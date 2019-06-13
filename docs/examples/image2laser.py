# Note: this needs to be executed from a terminal for gui functionality

from autopew.session import Session
from pathlib import Path
from autopew.util.writelase import xy2scansv

s = Session()
img = "NOR1-3B", Path("../../autopew/data/") / "images" / "NOR1-3B.jpg" # image
newpoints = Path("../../autopew/data/") / "NOR1-3B.csv" #
scancsv = Path("../../autopew/data/") / "_AutosavedScans.scancsv" # coordination points

newverts = s.autoflow(img, scancsv.resolve(), newpoints.resolve())

df = xy2scansv(newverts, spotname_prefix='NOR1-3B')

with open('testfile.scansv', 'wb') as f:
    str = df.to_csv(index=False).encode('utf-8')
    f.write(str)
