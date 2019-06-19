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

# %% Pixel Sample Points ------------------------------------------------------------
# Have some pixel coordinates ready?

pixel_sample_coords = np.array(
    [
        [831, 596],
        [166, 471],
        [835, 496],
        [807, 61],
        [981, 629],
        [341, 749],
        [746, 705],
        [773, 909],
        [159, 581],
        [219, 573],
        [846, 765],
        [88, 725],
        [20, 462],
        [757, 7],
        [317, 909],
        [181, 954],
        [810, 566],
        [434, 519],
    ]
)

# OR, Want to pick them from an image you have handy?
# pixel_sample_coords = pick_points(imagepath)

# %% Pixel Reference Points ------------------------------------------------------------
# Have some pixel coordinates ready?
# pixel_reference_coords = np.array([[0, 0], [10, 10], [10, 0], [0, 10]])
# OR, Want to pick them from an image you have handy?
pixel_reference_coords = pick_points(imagepath)

# %% Laser Reference Points ------------------------------------------------------------
# Have some laser coordinates ready?
laser_reference_coords = np.array(
    [[15000, 45000], [50000, 13000], [10000, 5000], [32000, 27000]]
)
# Want to import them from a .scancsv file?
# laser_reference_coords = np.array([[,], [,], [,]])
# Want to import them from a .csv file?
# laser_reference_coords = np.array([[,], [,], [,]])

# %% Calculate Transform ---------------------------------------------------------------
transform = affine_transform(
    affine_from_AB(pixel_reference_coords, laser_reference_coords)
)

# these are the magic points we want
laser_sample_coords = transform(pixel_sample_coords)

# %% Export to .Scancsv file -----------------------------------------------------------
# lets save them so we can directly impor them
points_to_scancsv(
    laser_sample_coords, filename=output_filename, spotname_prefix=spotname_prefix
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
