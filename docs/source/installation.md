# Installation


autopew is available on [PyPi](https://pypi.org/project/autopew/), and can be downloaded with pip:

```bash
pip install autopew
```

## Upgrading autopew


New versions of pyrolite are released frequently. You can upgrade to the latest edition
on [PyPi](https://pypi.org/project/autopew/) using the `--upgrade` flag:

```bash
pip install --upgrade autopew
```

## Development Installation

**autopew** is a work in progress. The development version is in a public
repository on [GitHub](https://github.com/morganjwilliams/autopew).
You can install it using pip directly from there:

```bash
pip install git+https://github.com/morganjwilliams/autopew.git#egg=autopew
# or, for the develop version
pip install git+https://github.com/morganjwilliams/autopew.git@develop#egg=autopew
```

Alternatively, you can also clone it locally and set up an environment with `uv`:

```bash
git clone https://github.com/morganjwilliams/autopew.git
cd autopew
uv sync
```

If you want to contribute to autopew, you might want to use an editable
installation locally to debug:

```bash
git clone https://github.com/morganjwilliams/autopew.git
cd autopew
uv sync
pip install -e .[dev]
```