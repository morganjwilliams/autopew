autopew
========

autopew is designed for arbitrary translation between planar/2D Cartesian coordinate
systems using affine transforms and human-in-the-loop workflows.

This is applied to integrating coordinate systems across analytical instrumentation,
with each instrument typically having its own individual coordinate systems based on
imagery and/or a sample stage.

**autopew** also includes functions for importing and exporting .lase files, for
automated generation of point sets within a relevant format.

.. image:: _static/transform_concept.png
   :align: center
   :width: 70%


What is **autopew** not?
----------------------

* Not currently capable of 3D affine transforms (i.e. no 'focus' attribute).

The current development plan for **autopew** can be found `here <future.html>`__.

.. toctree::
   :maxdepth: 1
   :hidden:

   installation
   usage/gettingstarted
   usage/examples
   tests
   docs
   future
   dev
   conduct

   submodules


.. note:: This documentation is a work in progress and is updated regularly. Contact
          the maintainers with any specific questions/requests.
