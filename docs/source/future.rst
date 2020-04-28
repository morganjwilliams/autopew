Future
========

This page details some of the under-development and planned features for
**autopew**. Note that while no schedules are attached, features under development
are likely to be completed with weeks to months, while those 'On The Horizon' may be
significantly further away (or in some cases may not make it to release).

Initial development focuses on work relevant to LA-ICP-MS workflows, and the project
may later generalise some of these workflows.


Current Release
-------------------

  * Able to register points on one image
  * Able to calibrate these points to the laser stage coordinates
  * Able to output the image with points on it
  * Able to output a .scancsv file to import into the laser software
  * Able to import point names

Under Development
-------------------

  * Be able to set spotsizes
  * Be able to read and set z position
  * Be able to recognise when point is positioned outside stage limits
  * Be able to transform maps with points on them so correspondence is easier to see
  * Should be able to work from multiple maps --> need multiple registered images
  * Overlay images (see post `here <https://stackabuse.com/affine-image-transformations-in-python-with-numpy-pillow-and-opencv/>`__)
  * Serialising coordinate transform systems for later use


On The Horizon
-------------------

* Activities to optimise instrument usage time:

  * Sample-standard bracketing using a specific 'reference mount location' (needs to be updated later)
  * Reordering points based on their positions.
  * Standard area registration, gridded 'free positions'- auto sample standard bracketing

* Report templates

* Dealing with larger images (>20 MB - jpg will warn of compression bomb)
