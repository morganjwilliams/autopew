Development
============

:code:`autopew` is currently hosted on GitHub at
`github.com/morganjwilliams/autopew <https://github.com/morganjwilliams/autopew>`__;
collaborator access can be granted to interested parties. If you're new to Git or GitHub,
there are some useful guides on the `GitHub Website <https://guides.github.com/>`__.

Branches and GitFlow
~~~~~~~~~~~~~~~~~~~~~~

There are two main git-branches for :code:`autopew`:

  * :code:`master` is the latest stable release.
  * :code:`develop` is the development branch.

The Git workflow is based on `GitFlow <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>`__,
where releases are branched from :code:`develop` prior to being integrated into
:code:`master`. Pull requests should be made against the :code:`develop` branch.

Documentation
---------------

Documentation is not currently live, but can be built and viewed locally using
instructions found on the `docs page <./docs.html>`__. The documentation is built using
`sphinx <http://www.sphinx-doc.org>`__, and most pages are written as
`reStructuredText <http://docutils.sourceforge.net/rst.html>`__. A quick reference
can be found `here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`__.


Continuous Integration
-----------------------

There are also some active continuous integration tools for :code:`autopew`, including
automated unit-testing on Travis-CI and test coverage analysis on Codecov. The details
for each of these are listed below.


**Travis-CI**

  The Travis-CI page for :code:`autopew` can be found at `travis-ci.com/morganjwilliams/autopew <https://travis-ci.com/morganjwilliams/autopew>`__.


**Code Coverage**

  The codecov page for :code:`autopew` can be found at `codecov.io/gh/morganjwilliams/autopew <https://codecov.io/gh/morganjwilliams/autopew>`__.
