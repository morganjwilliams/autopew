Image to Stage
===============

This is a simple workflow example involving converting points registered on an image
to coordinates for a specific stage.


Step 1: Acquire an Image and Register Points
---------------------------------------------

Once an image is acquired, points can be added (either via ImageJ, or through
**autopew** extensions). Optionally, add calibration points specifically for
calibrating the image-stage coordinate transform later on (3 points minimum, preferably
5-6 to average out inconsistencies and provide an accurate transform).

Step 2: Export Point Coordinates to CSV
-----------------------------------------

Export the pixel-coordinates of your planned points in X-Y(-Z) format to a CSV.
Optionally, specify names for each of the points, which could be used as an index
later.

Step 3: Calibrate the Transformation between the Image and Stage
-----------------------------------------------------------------

Pick a few calibration

Note that the calibration of this transform involves a least-squares process to find
the optimal transformation, such that adding more calibration points can help avoid
minor inaccuracies in adding points.

Step 4: Transform Image Point Coordinates to Stage Coordinates
---------------------------------------------------------------

  * Import your planned point pixel-coordinates from the CSV you saved earlier.
  * Use your calibrated Image-Stage transform to transform these points into stage coordinates.


Step 5: Export Points to for Stage Coordinates
-------------------------------------------------

  * Export the transformed point stage coordinates to a file you can import into the
      software controlling the stage.


Optional Next Steps
---------------------

  * Export an aligned image.

      Imported images can be realigned to the stage coordinate system for easier
      recognition of sample features and more accurate visual determination of new point
      location.
