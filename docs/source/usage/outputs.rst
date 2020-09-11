Output Types
=================
The output types can be edited to suit the equipment you wish to use.
The current output of coordinates are designed for the following analytical equipment.


Laser Ablation system
-------------------------------
The .scancsv current output is compatible with a Photonmachines (Teledyne) laser
running on `Chromium <http://www.teledynecetac.com/support/software>`__.
This allows for rapid input of X,Y coordinates into the laser system with spot
labels either read from the source file, or numbered sequentially.

Currently all other settings; including focus (z), spot size and laser conditions
need to be changed manually after import into the laser.

TESCAN SEM
-------------
**work in progress**

Use of the TESCAN SEM system allows input and output of .XML format coordinates.
Currently only allows export and import of a single .xml file per sample.
Multiple samples in a single .xml file is in development.

This export type does not include labels for points.

Focus is set per sample and needs to be manually adjusted for each analysis location.

JOEL EPMA
-----------
**work in progress**

autopew allows import and export of coordinates in .POS files. Compatible with
some JOEL EPMA devices.

Focus is set per sample and needs to be manually adjusted for each analysis location.

custom input and outputs
-----------------------------
autopew is designed for easy incorporation of your specific output file needs.
converting from a pandas dataframe containing X,Y and label, any output type can
be developed. Please see `the contributions page <../dev/contributing.html>`__.
for more information.
