Building Documentation
========================

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
