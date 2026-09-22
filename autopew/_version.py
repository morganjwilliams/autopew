from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("autopew")
except PackageNotFoundError:
    # package is not installed
    pass
