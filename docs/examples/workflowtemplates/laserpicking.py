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
pixel_sample_coords = np.array([[3, 8], [5, 2], [1, 0], [9, 8], [9, 9], [4, 3]])
# OR, Want to pick them from an image you have handy?
pixel_sample_coords = pick_points(imagepath)

# %% Pixel Reference Points ------------------------------------------------------------
# Have some pixel coordinates ready?
pixel_reference_coords = np.array([[0, 0], [10, 10], [10, 0], [0, 10]])
# OR, Want to pick them from an image you have handy?
pixel_reference_coords = pick_points(imagepath)

# %% Laser Reference Points ------------------------------------------------------------
# Have some laser coordinates ready?
laser_reference_coords = np.array(
    [[45000, 14000], [50000, 25000], [30000, 270000], [32000, 210000]]
)
# Want to import them from a .scancsv file?
# laser_reference_coords = np.array([[,], [,], [,]])
# Want to import them from a .csv file?
# pixel_reference_coordslaser_reference_coords = np.array([[,], [,], [,]])

# %% Calculate Transform ---------------------------------------------------------------
transform = affine_transform(
    affine_from_AB(pixel_reference_coords, laser_reference_coords)
)

laser_sample_coords = transform(pixel_sample_coords)

# %% Export to .Scancsv file -----------------------------------------------------------
points_to_scancsv(
    laser_sample_coords, filename=output_filename, spotname_prefix=spotname_prefix
)

# %% --
