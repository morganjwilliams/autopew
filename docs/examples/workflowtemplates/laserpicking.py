"""
This workflow is useful for picking points on an image prior to a laser session.

You will need pixel-based coordinates extracted from e.g. ImageJ, for both
your i) sample points and ii) your reference points (ideally, have 3-5 dedicated
reference points at the outer edges of your sample selection area). Note that adding
more reference points will help average out any positioning inaccuracy.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from autopew.workflow import pick_points
from autopew.workflow.laser import points_to_scancsv
from autopew.transform.affine import affine_transform, affine_from_AB

# have an image you wish to use?
imagepath = Path("./../../source/_static/") / "img.jpg"
# have an output filename you wish to use?
output_filename = Path("./") / "exportedpoints.scancsv"
# have a spot name prefix you wish to use?
spotname_prefix = "Spot"
# First we Need Some Coordinates.

# %% PIXEL SAMPLE POINTS ---------------------------------------------------------------
# Have some pixel coordinates ready?
pixel_sample_coords = np.array(
    [
        [831, 596],
        [166, 471],
        [807, 61],
        [981, 629],
        [341, 749],
        [746, 705],
        [773, 909],
        [159, 581],
        [757, 7],
        [317, 909],
        [181, 954],
        [810, 566],
        [434, 519],
    ]
)
# OR, Want to pick them from an image you have handy?
# pixel_sample_coords = pick_points(imagepath)

# %% PIXEL REFERENCE POINTS ------------------------------------------------------------
# Have some pixel coordinates ready?
# pixel_reference_coords = np.array([[0, 0], [10, 10], [10, 0], [0, 10]])
# OR, Want to pick them from an image you have handy?
pixel_reference_coords = pick_points(imagepath)

# %% LASER REFERENCE POINTS ------------------------------------------------------------

# Have some laser coordinates ready?
# laser_reference_coords = np.array([[15, 45], [50, 13], [10, 5], [32, 27]]) * 1000.0

# Want to import them from a .scancsv file?
from autopew.io.laser.readlase import read_scancsv

scancsvpath = Path("./../../../autopew/data/examples") / "autopew_test.scancsv"
l = read_scancsv(scancsvpath.resolve()).iloc[:3, 5]
items = zip(l.index, l.apply(lambda x: x[0][:2]))
laser_reference_coords = pd.DataFrame.from_items(items).T.astype(float)

# Want to import them from a .csv file?
# csvpath = Path("./../../../autopew/auotpew/data/examples") / "autopew_test.csv"
# laser_reference_coords = pd.read_csv(csvpath, sep=',')

# %% CALCULATE TRANSFORM ---------------------------------------------------------------
transform = affine_transform(
    affine_from_AB(pixel_reference_coords, laser_reference_coords)
)
# %% TRANSFORM SAMPLE POINTS -----------------------------------------------------------
# these are the magic points we want
laser_sample_coords = transform(pixel_sample_coords)

# %% EXPORT to .Scancsv file -----------------------------------------------------------
# lets save them so we can directly import them
spotnames = None
# have some spot names? add them here
# spotnames = df["Comment"]
points_to_scancsv(
    laser_sample_coords,
    filename=output_filename,
    spotnames=spotnames or spotname_prefix,
)
# %% Visualise the Transform
from autopew.util.plot import plot_transform

fig = plot_transform(
    pixel_sample_coords,
    tfm=transform,
    refpoints=pixel_reference_coords,
    invert0=[False, True],
    invert1=[False, True],
)
