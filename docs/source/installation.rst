Installation
================

autopew is available on `PyPi <https://pypi.org/project/autopew/>`_, and can be downloaded with pip:

.. code-block:: bash

   pip install autopew


.. note:: autopew is not yet packaged for Anaconda, and as such :code:`conda install autopew` will not work.


Upgrading autopew
--------------------

New versions of pyrolite are released frequently. You can upgrade to the latest edition
on `PyPi <https://pypi.org/project/autopew/>`_ using the :code:`--upgrade` flag:

.. code-block:: bash

  pip install --upgrade autopew



Development Installation
--------------------

**autopew** is a work in progress. The development version is in a public
repository on `GitHub <https://github.com/morganjwilliams/autopew>`_.
You can install it using pip directly from there:

.. code-block:: bash

   pip install git+https://github.com/morganjwilliams/autopew.git#egg=autopew
   # or, for the develop version
   pip install git+https://github.com/morganjwilliams/autopew.git@develop#egg=autopew

Alternatively, you can also clone it locally and install with pip:

.. code-block:: bash

  git clone https://github.com/morganjwilliams/autopew.git
  cd autopew
  # e.g if you navigate to the directory
  pip install .

If you want to contribute to autopew, you might want to use an editable
installation locally to debug:

.. code-block:: bash

  git clone https://github.com/morganjwilliams/autopew.git
  cd autopew
  # e.g if you navigate to the directory
  pip install -e .[dev]
