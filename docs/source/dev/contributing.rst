Contributing
=============

:mod:`autopew` welcomes community contributions of all forms.
Requests for features and bug reports are particularly valuable contributions,
in addition to code and expanding the documentation.

All individuals contributing to the project are expected to follow the
`Code of Conduct <../conduct.html>`__, which outlines community expectations and
responsibilities.

Also, be sure to add your name or GitHub username to the
`contributors list <./contributors.html>`__.

.. note:: This project is currently in `alpha`, and as such there's much work to be
          done.

Feature Requests
-------------------------

If you're new to Python, and want to implement something as part of :code:`autopew`,
you can submit a
`Feature Request <https://github.com/morganjwilliams/autopew/issues/new?labels=enhancement&template=feature-request.md>`__.
Perhaps also check the
`Issues Board <https://github.com/morganjwilliams/autopew/issues>`__ first to see if
someone else has suggested something similar (or if something is in development),
and comment there.

Bug Reports
-------------------------

If you've tried to do something with :code:`autopew`, but it didn't work, and googling
error messages didn't help (or, if the error messages are full of
:code:`autopew.XX.xx`), you can submit a
`Bug Report <https://github.com/morganjwilliams/autopew/issues/new?labels=bug&template=bug-report.md>`__ .
Perhaps also check the
`Issues Board <https://github.com/morganjwilliams/autopew/issues>`__ first to see if
someone else is having the same issue, and comment there.

Contributing to Documentation
------------------------------

The `documentation and examples <https://autopew.readthedocs.io>`__ for :code:`autopew`
are gradually being developed, and any contributions or corrections would be greatly
appreciated. Currently the examples are patchy, and a 'getting started' guide would be
a helpful addition. If you'd like to edit an existing page, the easiest way to
get started is via the 'Edit on GitHub' links:

.. image:: https://raw.githubusercontent.com/morganjwilliams/pyrolite/develop/docs/source/_static/editongithub.png
  :width: 100%
  :align: center
  :alt: Header found on each documentation page highlighting the "Edit on GitHub" link.

These pages serve multiple purposes:
  * A human-readable reference of the source code (compiled from docstrings).
  * A set of simple examples to demonstrate use and utility.
  * A place for developing extended examples

Contributing Code
-------------------------

Code contributions are always welcome, whether it be small modifications or entire
features. As the project gains momentum, check the
`Issues Board <https://github.com/morganjwilliams/autopew/issues>`__ for outstanding
issues, features under development. If you'd like to contribute, but you're not so
experienced with Python, look for :code:`good first issue` tags or email the maintainer
for suggestions.

To contribute code, the place to start will be forking the source for :code:`autopew`
from `GitHub <https://github.com/morganjwilliams/autopew/tree/develop>`__. Once forked,
clone a local copy and from the repository directory you can install a development
(editable) copy via :code:`python setup.py develop`. To incorporate suggested
changes back to into the project, push your changes to your
remote fork, and then submit a pull request onto
`autopew/develop <https://github.com/morganjwilliams/autopew/tree/develop>`__ .

.. note::

  * See `Installation <../installation.html>`__ for directions for installing extra
    dependencies for development, and `Development <development.html>`__ for information
    on development environments and tests.

  * :code:`autopew` development roughly follows a
    `gitflow workflow <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>`__.
    :code:`autopew/master` is only used for releases, and large separable features
    should be build on :code:`feature` branches off :code:`develop`.

  * Contributions introducing new functions, classes or entire features should
    also include appropriate tests where possible (see `Writing Tests`_, below).

  * :code:`autopew` uses `Black <https://github.com/python/black/>`__ for code formatting, and
    submissions which have passed through :code:`Black` are appreciated, although not critical.


Writing Tests
-------------------------

There is currently a minimal unit test suite for :code:`autopew`, which guards
against breaking changes and assures baseline functionality. :code:`autopew` uses continuous
integration via `Travis <https://travis-ci.org/morganjwilliams/autopew>`__, where the
full suite of tests are run for each commit and pull request, and test coverage output
to `Coveralls <https://coveralls.io/github/morganjwilliams/autopew>`__.

Adding or expanding tests is a helpful way to ensure :code:`autopew` does what is meant to,
and does it reproducibly. The unit test suite one critical component of the package,
and necessary to enable sufficient trust to use :code:`autopew` for scientific purposes.
