.. raw:: latex

   \chapter{Introduction}

autopew
========

autopew is designed for arbitrary translation between planar/2D Cartesian coordinate
systems using affine transforms and human-in-the-loop workflows.

This is applied to integrating coordinate systems across analytical instrumentation,
with each instrument typically having its own individual coordinate systems based on
imagery and/or a sample stage. **autopew** also includes functions for importing and
exporting files, for automated generation of point sets within a relevant format for
each piece of analytical instrumentation. **autopew** `outputs <usage/outputs.html>`__
currently included a .scancsv file which can be directly imported into
`Chromium <http://www.teledynecetac.com/support/software>`__
laser ablation navigation software.


Why use **autopew**
----------------------
**autopew** is designed for easy referencing between analytical equipment and/or images.
This allows the time spend on analytical equipment to be more effectively used for
data collection rather than spending valuable time locating the areas of interest.

This software also allows for tracking of the context of in-situ microanalysis by
allowing reference to large images and areas which will allow for new insights into
what effects chemistry of given particles with reference to their location and
micro-environment. We can then track the analysis between different analytical
equipment and make inferences on macroscale processes from well characterised
in-situ microanalysis [1]_.

Although primarily designed for use of laser ablation analysis on geological material
this software can be used for any microanalytical technique, including electron
microprobe analysis, x-ray fluorescence mapping, scanning electron
microscopy and ion beam analysis.

.. seealso::

  For outlined examples of how autopew is used, see `Examples <usage/examples.html>`__


What is **autopew** not?
-------------------------

* Not currently capable of 3D affine transforms (i.e. no 'focus' attribute).

The current development plan for **autopew** can be found `here <future.html>`__.

.. raw:: latex

   \chapter{Getting Started}

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Getting Started

    usage/gettingstarted
    installation


.. raw:: latex

  \chapter{Examples}

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Examples

   usage/usecases
   usage/examples
   usage/outputs


.. raw:: latex

 \chapter{Development}

.. toctree::
  :maxdepth: 1
  :hidden:
  :caption: Development

  API
  dev/development
  dev/changelog
  future
  conduct
  dev/contributing
  dev/contributors


.. note:: This documentation is a work in progress and is updated regularly. Contact
          the maintainers with any specific questions/requests.


References
-------------

.. [1] Pearce, M. A., Godel, B. M., Fisher, L. A., Schoneveld, L. E., Cleverly, J. S., Oliver, N. H. S., and  Nugus, M. (2017).
    Microscale data to macroscale processes: a review of microcharacterization applied to mineral
    systems: Geological Society, London, Special Publications,, v. 453
    `doi: 10.1144/SP453.3 <https://doi.org/10.1144/SP453.3>`__.
