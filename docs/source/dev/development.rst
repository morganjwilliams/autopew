Development
============

:code:`autopew` is currently hosted on GitHub at
`github.com/morganjwilliams/autopew <https://github.com/morganjwilliams/autopew>`__;
collaborator access can be granted to interested parties. If you're new to Git or GitHub,
there are some useful guides on the `GitHub Website <https://guides.github.com/>`__.


Development Installation
----------------------------

To access and use the development version, you can either
`clone the repository <https://github.com/morganjwilliams/autopew>`__ or install
via pip directly from GitHub:

.. code-block:: bash

  pip install git+git://github.com/morganjwilliams/autopew.git@develop#egg=autopew


Branches and GitFlow
---------------------

There are two main git-branches for :code:`autopew`:

  * :code:`master` is the latest stable release.
  * :code:`develop` is the development branch.

The Git workflow is based on `GitFlow <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>`__,
where releases are branched from :code:`develop` prior to being integrated into
:code:`master`. Pull requests should be made against the :code:`develop` branch.

Documentation
---------------

Documentation is currently live on `ReadtheDocs.org <https://autopew.readthedocs.io>`__`
, but can also be built and viewed locally using instructions below.
The documentation is built using `sphinx <http://www.sphinx-doc.org>`__, and most pages
are written in `reStructuredText <http://docutils.sourceforge.net/rst.html>`__.
A quick reference can be found
`here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`__.

Documentation for :mod:`autopew` is in the :code:`docs` directory. From this directory,
documentation can be built as follows:

To build documentation on windows:

.. code-block:: bash

   # to build and view the html version:
   make html && cd ./build/html/ && index.html && cd ../..
   # or, to build and view the latex-pdf version:
   make latex && cd ./build/latex/ && make.bat && autopew.pdf && cd ../..


Alternatively, there is a default build batch file :code:`makeviewhtml.bat` also located
in the docs directory, which executes the commands above and will automatically build
the docs and open the landing page:

.. code-block:: bash

   # to build and view the html version:
   makeviewhtml.bat


Tests
------

If you clone the source repository, unit tests can be run using pytest from the root
directory after installation:

.. code-block:: bash

   python setup.py test


Continuous Integration
-----------------------

.. image:: https://travis-ci.org/morganjwilliams/autopew.svg?branch=develop
    :target: https://travis-ci.org/morganjwilliams/autopew
    :alt: Test Status

.. image:: https://coveralls.io/repos/github/morganjwilliams/autopew/badge.svg?branch=develop
    :target: https://coveralls.io/github/morganjwilliams/autopew?branch=develop
    :alt: Test Coverage

There are also some active continuous integration tools for :code:`autopew`, including
automated unit-testing on Travis-CI and test coverage analysis on Codecov. The details
for each of these are listed below.

**Travis-CI**

  The Travis-CI page for :code:`autopew` can be found at `travis-ci.org/morganjwilliams/autopew <https://travis-ci.org/morganjwilliams/autopew>`__.

**Code Coverage**

  The coveralls page for :code:`autopew` can be found at `coveralls.io/github/morganjwilliams/autopew <https://coveralls.io/github/morganjwilliams/autopew>`__.
