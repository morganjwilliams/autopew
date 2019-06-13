# Note: this needs to be executed from a terminal for gui functionality

from autopew.session import Session
from pathlib import Path

s = Session()
img = "NOR1-3B", Path("../../autopew/data/") / "images" / "NOR1-3B.jpg"
newpoints = Path("../../autopew/data/") / "NOR1-3B.csv"
scancsv = Path("../../autopew/data/") / "_AutosavedScans.scancsv"

newverts = s.autoflow(img, scancsv.resolve(), newpoints.resolve())
print(newverts)
