Stage to Image
=================

This is a simple workflow example involving converting points from one stage coordinate
system to display on a large image. This helps to visualise where the analysis
were collected and gives context to the anaysis.

INPUT:
  * .csv - a list of X,Y coordinates with spotnames + more than 3 reference points
  * large image with locations of more than 3 reference points

OUTPUT:
  * image with points labelled

e.g. We have been using the workflow to visualise the microanalysis points from
SEM on large reflected light images

.. image:: ../../_static/stage2image_concept.png
  :align: center
  :width: 50%


Step 1: Acquire image
------------------------------

  * collect an image of the sample
  * Remember to highlight 3 regions or more for registration points


Step 2: Calibrate and Transform the points between the the image and the stage
--------------------------------------------------------------------------------

  * Import your CSV file with analysed points
  * specify your >3 reference coordinates using the **autopew** interacitve interface
  * specify the stage Coordinates of these reference points
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
  start_here = Path("./../../source/_static/")

  # %% INPUT STAGE ALL POINTS ---------------------------------------------------------------
  #import the coordinate from the source stage
  df = pd.read_csv('Analysis_Points.csv')
  #add the names of the points
  spotnames=df["ID"]
  #tell the code what the X,Y columns are named
  stage_sample_coords = np.array([df["X"],df["Y"]]).T

  # %% INPUT REFERENCE POINTS ------------------------------------------------------------
  # Pick reference points from the displayed image
  imagepath = start_here / "img.jpg"
  pixel_reference_coords = pick_points(imagepath)

  # %% STAGE REFERENCE POINTS ------------------------------------------------------------
  #Enter the coordinates for the reference points you chose
  stage_reference_coords = np.array([[-1300,-6120],  #R1
                                     [-8460,-1410], #R2
                                     [-1960,-1420], #R3
                                     [-6770,-6240]]) #R4

  # %% CALCULATE TRANSFORM ---------------------------------------------------------------
  transform = affine_transform(
    affine_from_AB(stage_reference_coords, pixel_reference_coords)
  )
  # %% TRANSFORM SAMPLE POINTS -----------------------------------------------------------
  # these are the magic points we want
  pixel_sample_coords = transform(stage_sample_coords)

Step 4: Overlay the image and the points
------------------------------------------------------

  * Export an image containing labelled point overlay over image

.. code-block:: bash

  # %% GIVE NAMES TO THE NEW POINTS -----------------------------------------------------------
  new_coords=pd.DataFrame(data=pixel_sample_coords[0:,0:], columns=['x','y'])
  new_coords["ID"]=spotnames

  # %% FIND THE PIXEL SIZE OF THE IMAGE---------------------------------------------------------
  from PIL import Image

  img = Image.open(imagepath)
  # get the image's width and height in pixels
  width, height = img.size

  # %% PLOT THE POINTS ON THE IMAGE---------------------------------------------------------
  import matplotlib.pyplot as plt

  X=new_coords['x']
  Y=new_coords['y']
  label=new_coords['ID']

  fig, ax = plt.subplots()
  ax.scatter(X, Y,color='yellow', marker="+",zorder=1,s=6,linewidth=.3)

  for i, df in enumerate(label):
      ax.annotate(df, (X[i], Y[i]),
                  xytext=(2, 0), textcoords='offset points',
                  horizontalalignment='left', verticalalignment='center',
                  size=2, color='yellow',
                  zorder=1)
  ax.set(xlim=(0, width), ylim=(0, height))

  plt.imshow(img, zorder=0)
  ax.invert_yaxis()#image invert so it is the same up direction as import.

  plt.show()
  #fig.savefig('temp.png', transparent=True, dpi=800) #Optional Image Export


.. seealso::

  `output types <../outputs.html>`__
