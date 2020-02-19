Stage to Stage
=================

This is a simple workflow example involving converting points from one stage coordinate
system to another.

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
  * Use **autopew** to transform all stage coordinates


Note that the calibration of this transform involves a least-squares process to find
the optimal transformation, such that adding more calibration points can help avoid
minor inaccuracies in adding points.


Step 4: Export Points to for new Stage Coordinates
------------------------------------------------------

  * Export the transformed point stage coordinates to a file you can import into the software controlling the new stage.


.. seealso::

  `output types <../outputs.html>`__
