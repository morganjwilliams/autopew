Stage to Stage
=================

This is a simple workflow example involving converting points from one stage coordinate
system to another. This workflow also works for importing .csv files of pixel x,y
coordinates from software such as imageJ.

INPUT: .csv - a list of X,Y coordinates with spotnames + more than 3 reference points

OUTPUT: scancsv file in laser coordinate system with corresponding spotnames

e.g. We have been using the workflow to ensure measurement of the
same grain on both scanning electron microscope and the laser ablation system.


Step 1: Acquire coordinates
------------------------------

  * save the coordinates of 3 or more registration points
  * collect and save coordinates of phases of interest


Step 2: Export Point Coordinates to CSV
---------------------------------------------

  * Export the stage-coordinates of your planned points in X-Y(-Z) format to a CSV.


Optionally, specify names for each of the points, which could be used as an index
later.


Step 3: Calibrate and Transform the points between the two stages
---------------------------------------------------------------------

  * Import your origin CSV file
  * specify your >3 reference coordinates
  * give the same points in the new stage Coordinates
  * Use **autopew** to transform all stage coordinates. See the example code below:

Note that the calibration of this transform involves a least-squares process to find
the optimal transformation, such that adding more calibration points can help avoid
minor inaccuracies in adding points.

.. code-block:: bash

  import numpy as np
  import pandas as pd
  from pathlib import Path
  from autopew.workflow import pick_points
  from autopew.workflow.laser import points_to_scancsv
  from autopew.transform.affine import affine_transform, affine_from_AB

  # let the code know what folder we are working in:
  start_here = Path(r"C:\FILEPATH")

  # First we Need Some Coordinates.
  # %% INPUT STAGE ALL POINTS ---------------------------------------------------------------
  #import the coordinate from the source stage
  df = pd.read_csv(start_here/"LaserPoints.csv")
  #drop any blank rows
  df = df.dropna(how='all', axis='index')
  #add the names of the points
  spotnames=df["PointName"]
  #tell the code what the X,Y columns are named
  pixel_sample_coords = np.array([df["X"],df["Y"]]).T

  # %% INPUT STAGE REFERENCE POINTS ------------------------------------------------------------
  pixel_reference_coords = np.array([
        [-26369.84,-35504.5],  #R1
        [-10899.56,-34236.77], #R2
        [-18028.68,-25400.77], #R3
        [-18679.94,-25251.63]])#R4

  # %% OUTPUT STAGE REFERENCE POINTS ------------------------------------------------------------
  laser_reference_coords = np.array([
        [74978,85419],   #R1
        [90828,82571],   #R2
        [80259,75389],   #R3
        [81465,74373]])  #R4


  # %% CALCULATE TRANSFORM ---------------------------------------------------------------
  transform = affine_transform(
    affine_from_AB(pixel_reference_coords, laser_reference_coords)
  )
  # %% TRANSFORM SAMPLE POINTS -----------------------------------------------------------
  # these are the magic points we want
  laser_sample_coords = transform(pixel_sample_coords)

  # %% Visualise the Transform
  from autopew.util.plot import plot_transform

  fig = plot_transform(
    pixel_sample_coords,
    tfm=transform,
    ref=pixel_reference_coords,
    invert0=[False, True],
    invert1=[False, True],)


Step 4: Export Points to for new Stage Coordinates
------------------------------------------------------

  * Export the transformed point stage coordinates to a file you can import into the software controlling the new stage.

.. code-block:: bash

  # %% EXPORT to .Scancsv file -----------------------------------------------------------
  # lets save them so we can directly import them
  points_to_scancsv(
    laser_sample_coords, filename="output_filename", spotnames=spotnames
  )


.. seealso::

  `output types <../outputs.html>`__
