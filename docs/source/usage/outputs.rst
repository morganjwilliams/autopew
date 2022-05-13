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

Currently all other settings; including fine focus (z), spot size and laser conditions
need to be changed manually after import into the laser.

JEOL EPMA
---------------
The .pos files for the JEOL field-emission gun electron probe microanalyser (EPMA)
using "probe for EPMA" software. A default z value can be assigned for each export
however fine focus will need to be changed manually.

TESCAN SEM
-------------

**Work in Progress**

Use of the TESCAN SEM system allows input and output of .XML format coordinates.
Currently only allows export and import of a single .xml file per sample.
Multiple samples in a single .xml file is in development.

This export type does not include labels for points.

Focus is set per sample and needs to be manually adjusted for each analysis location.

Adding New IO Functionality
---------------------------

New file types can be configured around the :class:`autopew.io.PewIOSpecification`
interface, as have been done for the above instruments. These will be automatically
registered as file handlers where the file extension is unique.
For example, see the soure code specification for :class:`autopew.io.PewSCANCSV`
which includes a function for reading `.scancsv` files into a consistent format
and outputting data from that format into `.scancsv` files.
