Image to Stage
===============

This is a simple workflow example involving converting points registered on an image
to coordinates for a specific stage.

e.g we have been using this method to extract phases from reflected light
imagery or X-ray fluorescence mapping and assign numbers to grains to give
spatial context to the multiple different micro-geochemical analysis. 


Step 1: Acquire an Image and Register Points
---------------------------------------------

  * Aquire an image of your sample
  * add points to your image

Once an image is acquired, points can be added (either via `ImageJ or Fiji <https://imagej.net/Welcome>`__ [*]_
, or through **autopew** extensions). Optionally, add calibration points specifically for
calibrating the image-stage coordinate transform later on (3 points minimum, preferably
5-6 to average out inconsistencies and provide an accurate transform).



Step 2: Export Point Coordinates to CSV
-----------------------------------------

  * Export the pixel-coordinates of your planned points in X-Y(-Z) format to a CSV.

Optionally, specify names for each of the points, which could be used as an index
later.


Step 3: Calibrate the Transformation between the Image and Stage
-----------------------------------------------------------------

  * Pick a 3 or more calibration points

Note that the calibration of this transform involves a least-squares process to find
the optimal transformation, such that adding more calibration points can help avoid
minor inaccuracies in adding points.


Step 4: Transform Image Point Coordinates to Stage Coordinates
---------------------------------------------------------------

  * Import your pixel CSV file
  * specify your >3 reference points from your pixel coordinates
  * give the same points in the stage Coordinates
  * Use **autopew** to transform all pixel coordinates to stage coordinates


Step 5: Export Points to for Stage Coordinates
-------------------------------------------------

  * Export the transformed point stage coordinates to a file you can import into the software controlling the stage.

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
