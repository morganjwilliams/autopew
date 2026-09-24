# Changelog

All notable changes to this project will be documented here.

## Development

:::{note}
Changes noted in this subsection are to be released in the next version.
        If you're keen to check something out before its released, you can use a
        [development install](development.md#development-installation).
:::


## 0.1.1

* Expanded development documentation.
* Updated installation instructions.
* Added basic documentation examples and a workflow runthrough.
* Added a network-based transformation concept example.

### {py:mod}`autopew.transform`

* Added {py:class}`autopew.transform.CoordinateTransform`, inverse affine transform

## 0.0.2

* Added PyQT requirement for GUI-based point-picking.

### {py:mod}`autopew.gui`

* Update for GUI point selection to add refreshing timeout.
* Renamed {py:func}`~autopew.gui.image_registration` to
  {py:func}`~autopew.gui.image_point_registration`; later moved to
  {py:func}`autopew.util.gui.image_point_registration`
* Added differentiated handling of mouse events for panning, zooming and clicking
  in {py:mod}`autopew.util.gui`

### {py:mod}`autopew.registration`

* Updated {py:class}`autopew.registration.RegisteredImage` image handling to
  allow load from path/array/existing image.
* Added {py:meth}`~autopew.registration.RegisteredImage.set_calibration_pixelpoints`
  for setting calibration points for a registered image.

### {py:mod}`autopew.session`

* Added {py:meth}`~autopew.session.Session.load_image`,
  {py:meth}`~autopew.session.Session.points_from_csv`,
  {py:meth}`~autopew.session.Session.autoflow` and stubs for
  {py:meth}`~autopew.session.Session.reorder_analyses`,
  {py:meth}`~autopew.session.Session.standard_bracket` (neither implemented
  in this version).
* Added an automated workflow for export of coordinates from a CSV, image
  and stage coordinates in {py:meth}`~autopew.session.Session.autoflow`.

### {py:mod}`autopew.transform`

* Added a `rcond` switch for {py:func}`numpy.linalg.lstsq` for `Python <= 3.6` in
  {py:meth}`autopew.transform.calibration` due to recurring errors.

### {py:mod}`autopew.util`

* Added {py:meth}`autopew.util.readlase` for reading specific laser analysis files.

## 0.0.1

* First version of the package, with capability for basic point-point and
  image-point calibration/registration.
* Added submodules {py:meth}`autopew.session`, {py:meth}`autopew.targets`,
  {py:meth}`autopew.gui`, {py:meth}`autopew.transform.calibration`,
  {py:meth}`autopew.registration`, {py:meth}`autopew.util`
* Added some basic tests.

