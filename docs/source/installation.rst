Installation
================

:code:`autopew` is a private repo on `GitHub <https://github.com/morganjwilliams/autopew>`_.
If you have access on github, you can install it with pip (you may be prompted for user-password):

.. code-block:: bash

   pip install git+https://github.com/morganjwilliams/autopew.git#egg=autopew
   # or, for the develop version
   pip install git+https://github.com/morganjwilliams/autopew.git@develop#egg=autopew

Alternatively, you can also clone it locally and install with pip:

.. code-block:: bash

  pip install -e <repo-directory>


Optional dependencies (`dev`, `gui`) can be specified during pip installation.
For example:

.. code-block:: bash

   pip install autopew[dev]

   pip install autopew[dev,gui]
