from autopew.session import Session

s = Session()
img = "NOR1-3B", Path("./data/") / "images" / "NOR1-3B.jpg"
newpoints = Path("./data/") / "NOR1-3B.csv"
scancsv = Path("./data/") / "_AutosavedScans.scancsv"
newverts = s.autoflow(img, scancsv, newpoints)
print(newverts)
