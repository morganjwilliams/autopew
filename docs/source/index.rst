autopew
========

autopew is designed for arbitrary translation between planar/2D Cartesian coordinate
systems using affine transforms and human-in-the-loop workflows.

This is applied to integrating coordinate systems across analytical instrumentation,
with each instrument typically having its own individual coordinate systems based on
imagery and/or a sample stage. **autopew** also includes functions for importing and
exporting files, for automated generation of point sets within a relevant format for
each piece of analytical instrumentation. **autopew** `outputs <usage/outputs.html>`__
currently included a .scancsv file which can be directly imported into `Chromium <http://www.teledynecetac.com/support/software>`__
laser ablation navigation software.

.. image:: _static/transform_concept.png
   :align: center
   :width: 70%


What is **autopew** not?
-------------------------

* Not currently capable of 3D affine transforms (i.e. no 'focus' attribute).

The current development plan for **autopew** can be found `here <future.html>`__.

.. toctree::
   :maxdepth: 1
   :hidden:

   installation
   usage/gettingstarted
   usage/examples
   submodules
   dev/development
   dev/changelog
   future
   conduct
   dev/contributing
   dev/contributors


.. note:: This documentation is a work in progress and is updated regularly. Contact
          the maintainers with any specific questions/requests.
