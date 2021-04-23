Changelog
=============


All notable changes to this project will be documented here.

`Development`_
---------------

.. note:: Changes noted in this subsection are to be released in the next version.
        If you're keen to check something out before its released, you can use a
        `development install <development.html#development-installation>`__.

`0.1.3`_
--------------


`0.1.2`_
--------------


`0.1.1`_
--------------

* Expanded development documentation.
* Updated installation instructions.
* Added basic documentation examples and a workflow runthrough.
* Added a network-based transformation concept example.

:mod:`autopew.transform`
~~~~~~~~~~~~~~~~~~~~~~~~

* Added :class:`autopew.transform.CoordinateTransform`, inverse affine transform


`0.1.0` (Unreleased)
----------------------


`0.0.2`_
--------------

* Added PyQT requirement for GUI-based point-picking.

:mod:`autopew.gui`
~~~~~~~~~~~~~~~~~~~~~~~~
* Update for GUI point selection to add refreshing timeout.
* Renamed :func:`~autopew.gui.image_registration` to
  :func:`~autopew.gui.image_point_registration`; later moved to
  :func:`autopew.util.gui.image_point_registration`
* Added differentiated handling of mouse events for panning, zooming and clicking
  in :mod:`autopew.util.gui`

:mod:`autopew.registration`
~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Updated :class:`autopew.registration.RegisteredImage` image handling to
  allow load from path/array/existing image.
* Added :meth:`~autopew.registration.RegisteredImage.set_calibration_pixelpoints`
  for setting calibration points for a registered image.

:mod:`autopew.session`
~~~~~~~~~~~~~~~~~~~~~~~
* Added :meth:`~autopew.session.Session.load_image`,
  :meth:`~autopew.session.Session.points_from_csv`,
  :meth:`~autopew.session.Session.autoflow` and stubs for
  :meth:`~autopew.session.Session.reorder_analyses`,
  :meth:`~autopew.session.Session.standard_bracket` (neither implemented
  in this version).
  * Added an automated workflow for export of coordinates from a CSV, image
    and stage coordinates in :meth:`~autopew.session.Session.autoflow`.

:mod:`autopew.transform`
~~~~~~~~~~~~~~~~~~~~~~~~
* Added a `rcond` switch for :func:`numpy.linalg.lstsq` for `Python <= 3.6` in
  :mod:`autopew.transform.calibration` due to recurring errors.

:mod:`autopew.util`
~~~~~~~~~~~~~~~~~~~~~~~~
* Added :mod:`autopew.util.readlase` for reading specific laser analysis files.


`0.0.1`_
--------------

* First version of the package, with capability for basic point-point and
  image-point calibration/registration.
* Added submodules :mod:`autopew.session`, :mod:`autopew.targets`,
  :mod:`autopew.gui`, :mod:`autopew.transform.calibration`,
  :mod:`autopew.registration`, :mod:`autopew.util`
* Added some basic tests.


.. _Development: https://github.com/morganjwilliams/autopew/compare/0.1.3...develop
.. _0.1.3: https://github.com/morganjwilliams/autopew/compare/0.1.2...0.1.3
.. _0.1.2: https://github.com/morganjwilliams/autopew/compare/0.1.1...0.1.2
.. _0.1.1: https://github.com/morganjwilliams/autopew/compare/0.0.2...0.1.1
.. _0.0.2: https://github.com/morganjwilliams/autopew/compare/0.0.1...0.0.2
.. _0.0.1: https://github.com/morganjwilliams/autopew/releases/tag/0.0.1
