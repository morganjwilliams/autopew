Image to Stage
===============

This is a simple workflow example involving converting points registered on an image
to coordinates for a specific stage.

INPUT: image of sample

OUTPUT: scancsv file in laser coordinate system with corresponding spotnames + realigned image

e.g we have been using this method to extract phases from reflected light
imagery or X-ray fluorescence mapping and assign numbers to grains to give
spatial context to the multiple different micro-geochemical analysis.

.. image:: ../../_static/img.jpg
  :align: center
  :width: 50%


Step 1: Acquire an Image and Register Points
---------------------------------------------

  * Aquire an image of your sample
  * add points to your image


Once an image is acquired, points can be added (either via `ImageJ or Fiji <https://imagej.net/Welcome>`__ [*]_
, or through **autopew** extensions).  If you use ImageJ, export your points as a .csv file and follow
the `Stage to stage <stage2stage.html>`__ workflow which outlines transforming a
list of X,Y coordinates into a new translation. The following workflow is designed using the
**autopew** extensions.

For selection points directly in **autopew** here is an example:

.. code-block:: bash

  import numpy as np
  import pandas as pd
  from pathlib import Path
  from autopew.workflow import pick_points
  from autopew.workflow.laser import points_to_scancsv
  from autopew.transform.affine import affine_transform, affine_from_AB

  # have an image you wish to use?
  imagepath = Path("./../../source/_static/") / "img.jpg"

  # pick coordinates from an image you have handy?
  pixel_sample_coords = pick_points(imagepath)


Step 3: Calibrate the Transformation between the Image and Stage
-----------------------------------------------------------------

  * Pick a 3 or more calibration points

Note that the calibration of this transform involves a least-squares process to find
the optimal transformation, such that adding more calibration points can help avoid
minor inaccuracies in adding points.

.. code-block:: bash
  # pick reference coordinates on image
  pixel_reference_coords = pick_points(imagepath)

Step 4: Transform Image Point Coordinates to Stage Coordinates
---------------------------------------------------------------

  * give the same reference points in the stage Coordinates (laser reference coordinates)
  * Use **autopew** to transform all pixel coordinates to stage coordinates. See the example code below:

.. code-block:: bash

  # %% LASER REFERENCE POINTS ------------------------------------------------------------
  laser_reference_coords = np.array([
        [74978,85419],
        [90828,82571],
        [80259,75389],
        [81465,74373]])


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


Step 5: Export Points to for Stage Coordinates
-------------------------------------------------

  * Export the transformed point stage coordinates to a file you can import into the software controlling the stage.

.. code-block:: bash

  # %% EXPORT to .Scancsv file -----------------------------------------------------------
  # lets save them so we can directly import them
  points_to_scancsv(
    laser_sample_coords, filename="output_filename", spotnames=spotnames
  )


.. seealso::

  `output types <../outputs.html>`__

Optional Next Steps
---------------------

  * Export an aligned image.

Imported images can be realigned to the stage coordinate system for easier
recognition of sample features and more accurate visual determination of new point
location.


References
~~~~~~~~~~~

  .. [*] Schneider, C. A.; Rasband, W. S. & Eliceiri, K. W. (2012), "NIH Image
    to ImageJ: 25 years of image analysis", Nature methods 9(7): 671-675, PMID 22930834
