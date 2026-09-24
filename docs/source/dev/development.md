# Development

`autopew` is currently hosted on GitHub at
[github.com/morganjwilliams/autopew](https://github.com/morganjwilliams/autopew);
collaborator access can be granted to interested parties. If you're new to Git or GitHub,
there are some useful [guides on the GitHub Website](https://guides.github.com).

## Development Installation

To access and use the development version, you can either [clone the repository](https://github.com/morganjwilliams/autopew)
and use `uv sync`or install via `pip` directly from GitHub:

```bash
pip install git+git://github.com/morganjwilliams/autopew.git@develop#egg=autopew
```
## Branches and GitFlow

There are two main git-branches for `autopew`:

  * `master` is the latest stable release.
  * `develop` is the development branch.

The Git workflow is based on [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow),
where releases are branched from `develop` prior to being integrated into
`master`. Pull requests should be made against the `develop` branch.

## Documentation

Documentation is currently live on [ReadtheDocs.org]'(https://autopew.readthedocs.io), 
but can also be built and viewed locally using instructions below.
The documentation is built using [Sphinx](http://www.sphinx-doc.org), and most pages
are written in Markdown/MyST Markdown (e.g. [see here for a guide](https://mystmd.org/guide)).

Documentation for `autopew` is in the `docs` directory. From this directory,
documentation can be built as follows:

To build documentation on Windows:

```bash
# to build and view the html version:
make html && cd ./build/html/ && index.html && cd ../..
# or, to build and view the latex-pdf version:
make latex && cd ./build/latex/ && make.bat && autopew.pdf && cd ../..
```

Alternatively, there is a default build batch file `makeviewhtml.bat` also located
in the docs directory, which executes the commands above and will automatically build
the docs and open the landing page:

```bash
# to build and view the html version on windows
makeviewhtml.bat
```

## Tests

If you clone the source repository, unit tests can be run using pytest from the root
directory after installation:

```bash
python setup.py test
```

## Continuous Integration

There are also some active continuous integration tools for `autopew`, including
automated unit-testing on GitHub actions and test coverage analysis on Coveralls;
links and statuses for these are shown immediately below.

```{image} https://github.com/morganjwilliams/pyrolite/actions/workflows/unittest.yml/badge.svg?branch=develop
:alt: Test Status
:target: https://github.com/morganjwilliams/autopew/actions?query=workflow:Unittest+branch:develop
```

```{image} https://coveralls.io/repos/github/morganjwilliams/autopew/badge.svg?branch=develop
:alt: Test Coverage
:target: https://coveralls.io/github/morganjwilliams/autopew?branch=develop
```